# -*- coding: utf-8 -*-
import scrapy
import requests
import random
import json
import re
import os
from bs4 import BeautifulSoup
from PIL import Image


class BuySpider(scrapy.Spider):
    name = 'miaosha'
    allowed_domains = ['jd.com']
    commodity_url = 'https://item.jd.com/875551.html'
    folderpath = '/Users/lujianqiang/Development/work/jingdong/results/'
    cookiespath = '/Users/lujianqiang/Development/work/jingdong/cookies.txt'
    info = []

    def writeresponse2file(self, response, filename):
        with open('{}/{}'.format(response.meta['path'], filename), 'w') as f:
            f.write(response.text + '\n======\n\n\n')
            f.write(str(response.headers) + '======\n\n\n')
            for key, value in response.meta['cookies'].items():
                f.write('{} : {}\n'.format(key, value))

    def jsonfy_cookies(self, raw_cookies):
        try:
            cookies_items = re.findall('([^;]+)', raw_cookies)
            cookies = {}
            for cookies_item in cookies_items:
                key = cookies_item[:cookies_item.find('=')]
                value = cookies_item[cookies_item.find('=') + 1:]
                cookies[key.strip()] = value.strip()
            return cookies
        except:
            print('raw_cookies出错')
            return {}

    def set_cookie(self, headers, cookies):
        if 'Set-Cookie' in headers:
            set_cookies = headers['Set-Cookie'].decode('UTF-8')
            key = re.findall('([^=]+)=', set_cookies)[0]
            if '"' in set_cookies:
                value = re.findall('="([^"]*)', set_cookies)[0]
            else:
                value = re.findall('=([^;]*)', set_cookies)[0]
            cookies[key] = value
            return cookies

    def start_requests(self):
        with open(self.cookiespath) as f:
            for i, line in enumerate(f.readlines()):
                self.info.append({
                    'commodity_url': self.commodity_url,
                    'cookies': self.jsonfy_cookies(line),
                    'path': self.folderpath + str(i)
                })
        for info in self.info:
            info['i'] = i
            info['dont_redirect'] = True
            info['handle_httpstatus_list'] = [302]
            if os.path.exists(info['path']):
                pass
            else:
                os.mkdir(info['path'])
            commodity_id = re.findall('(\d+)', info['commodity_url'])[0]
            info['commodity_id'] = commodity_id
            commodity_count = 1
            url = 'https://yushou.jd.com/youshouinfo.action?sku={}'.format(
                commodity_id)
            yield scrapy.Request(url, callback=self.youshou, meta=info, dont_filter=True)

    def youshou(self, response):
        self.writeresponse2file(response, 'youshou.html')
        url = 'https:{}'.format(json.loads(response.text)['url'])
        yield scrapy.Request(url, callback=self.qianggou, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def qianggou(self, response):
        self.writeresponse2file(response, 'qianggou.html')
        if 'Location' in response.headers:
            url = response.headers['Location'].decode('UTF-8')
            yield scrapy.Request(url, callback=self.gate, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)
        else:
            print('抢购未开始')

    def gate(self, response):
        self.writeresponse2file(response, 'gate.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = response.headers['Location'].decode('UTF-8')
        yield scrapy.Request(url, callback=self.addToCart, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def addToCart(self, response):
        self.writeresponse2file(response, 'addToCart.html')
        meta = response.meta
        commodity_id = meta['commodity_id']
        meta['rid'] = re.findall('rid=([\.\d]+)', response.url)[0]
        meta['commodity_id'] = commodity_id
        url = 'https://cart.jd.com/tproduct?pid={}'.format(commodity_id)
        yield scrapy.FormRequest(url, callback=self.tproduct, cookies=response.meta['cookies'], meta=meta, dont_filter=True)

    def tproduct(self, response):
        self.writeresponse2file(response, 'tproduct.html')
        if not json.loads(response.text)['success']:
            print('加入购物车失败')
            return
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/dynamic/consignee/getConsigneeList.action?charset=UTF-8'
        yield scrapy.Request(url, callback=self.getConsigneeList, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def getConsigneeList(self, response):
        self.writeresponse2file(response, 'getConsigneeList.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/order/getOrderInfo.action?rid={}'.format(response.meta[
            'rid'])
        yield scrapy.Request(url, callback=self.getOrderInfo, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def getOrderInfo(self, response):
        self.writeresponse2file(response, 'getOrderInfo.html')
        print(json.dumps(response.headers))
        return
        self.set_cookie(response.headers, response.meta['cookies'])
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            consignee_id = soup.find('input', id='consignee_id').attrs['value']
        except AttributeError:
            print('下单中……')
            return
        response.meta['consignee_id'] = consignee_id
        response.meta['riskControl'] = soup.find(
            'input', id='riskControl').attrs['value']
        response.meta['showCheckCode'] = soup.find(
            'input', id='showCheckCode').attrs['value']
        response.meta['encryptClientInfo'] = soup.find(
            'input', id='encryptClientInfo').attrs['value']
        response.meta['sopNotPutInvoice'] = soup.find(
            'input', id='sopNotPutInvoice').attrs['value']
        response.meta['proxy'] = 'https://localhost:8888'
        formdata = {
            'consigneeParam.id': str(consignee_id),
            'consigneeParam.addType': '0'
        }
        url = 'https://trade.jd.com/shopping/dynamic/coupon/getCoupons.action'
        yield scrapy.FormRequest(url, formdata=formdata, callback=self.getCoupons, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def getCoupons(self, response):
        self.writeresponse2file(response, 'getCoupons.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/dynamic/coupon/checkFundsPwdResult.action'
        formdata = {
            'couponParam.fundsPwdType': 'dongfreightPwdType'
        }
        yield scrapy.FormRequest(url, formdata=formdata, callback=self.checkFundsPwdResult, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def checkFundsPwdResult(self, response):
        self.writeresponse2file(response, '.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/dynamic/payAndShip/getAdditShipment.action'
        formdata = {
            'paymentId': '1',
            'shipParam.reset311': '0',
            'resetFlag': '1000000000',
            'shipParam.onlinePayType': '0',
            'typeFlag': '0',
            'promiseTagType': ''
        }
        yield scrapy.FormRequest(url, formdata=formdata, callback=self.getAdditShipment, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def getAdditShipment(self, response):
        self.writeresponse2file(response, 'getAdditShipment.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/dynamic/order/isNeedPaymentPassword.action'
        yield scrapy.FormRequest(url, callback=self.isNeedPaymentPassword1, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def isNeedPaymentPassword1(self, response):
        self.writeresponse2file(response, 'isNeedPaymentPassword1.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/dynamic/order/isNeedPaymentPassword.action'
        yield scrapy.FormRequest(url, callback=self.isNeedPaymentPassword2, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def isNeedPaymentPassword2(self, response):
        self.writeresponse2file(response, 'isNeedPaymentPassword2.html')
        self.set_cookie(response.headers, response.meta['cookies'])
        url = 'https://trade.jd.com/shopping/order/submitOrder.action'
        formdata = {
            'overseaPurchaseCookies': '',
            'submitOrderParam.sopNotPutInvoice': response.meta['sopNotPutInvoice'],
            'submitOrderParam.trackID': '1EnZznHbi_osE0j7gmkydPMDLdyFMihE9eo93Pn98Llc4HOQo3jmh4HSEIWvwVENVc-aY6DeW398bGxcEsWOnXiQKHE-KhQP1Xrtxgkkdti6WPCuZe6HgeRwXuwsfcyWu',
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'submitOrderParam.eid': '2B2TLATCMZ2WZW2K4WXKYDRQ5ERE3IK2KUTJV3NNRWPXUE3PS65TPSVQOOGHKTXCR2DMLRH5X55IONEMYQ23ZQYWIM',
            'submitOrderParam.fp': '1bfd483e16b5ff63c4296a8df507b879',
            'riskControl': response.meta['riskControl']
        }
        if response.meta['showCheckCode']:
            rid = '{}_{}'.format(random.random(), random.random())
            checkcodeurl = 'https://captcha.jd.com/verify/image?acid={}&srcid=trackWeb&is={}'.format(rid,
                                                                                                     response.meta['encryptClientInfo'])
            with open('checkcode.jpg', 'wb') as f:
                f.write(requests.get(checkcodeurl,
                                     cookies=response.meta['cookies']).content)
            img = Image.open('checkcode.jpg')
            img.show()
            img.close()
            formdata[
                'submitOrderParam.checkCodeRid'] = rid
            formdata['submitOrderParam.checkcodeTxt'] = input('请输入验证码:\n')
        yield scrapy.FormRequest(url, formdata=formdata, callback=self.submitOrder, cookies=response.meta['cookies'], meta=response.meta, dont_filter=True)

    def submitOrder(self, response):
        print(response.text)
        self.writeresponse2file(response, 'submitOrder.html')
        ok = 0
        try:
            data = json.loads(response.text)
            response.meta['account'] = data['pin']
            response.meta['success'] = data['success']
            response.meta['needCheckCode'] = data['needCheckCode']
            response.meta['orderId'] = data['orderId']
            response.meta['number'] = data['submitSkuNum']
            if data['success']:
                ok = 1
                print('{}[{}]下单成功，数量{}，单号是[{}]，请及时付款。'.format(
                    response.meta['i'], data['pin'], data['submitSkuNum'], data['orderId']))
            else:
                print('{}[{}]下单中……'.format(response.meta['i'], data['pin']))
        except json.decoder.JSONDecodeError:
            print('下单中……')
        with open('{}/{}'.format(response.meta['path'], 'info.txt'), 'w') as f:
            for key, value in response.meta.items():
                f.write('{} : {}\n'.format(key, value))
        if not ok:
            return
            url = 'https://cart.jd.com/batchRemoveSkusFromCart.action'
            data = {
                'null': '',
                't': '0',
                'outSkus': '',
                'random': '0.4370122519666315',
                'locationId': '1 - 72 - 2839 - 0'
            }
            yield scrapy.Request(url, callback=self.batchRemoveSkusFromCart,
                                 cookies=response.meta[
                                     'cookies'], dont_filter=True,
                                 meta=response.meta)

    def batchRemoveSkusFromCart(self, response):
        data = json.loads(response.text)['sortedWebCartResult']
        if data['success']:
            print('从购物车中删除商品成功')
        else:
            print('从购物车中删除商品中……')
        if data['modifyResult']['cartIsEmpty']:
            print('购物车已清空')
