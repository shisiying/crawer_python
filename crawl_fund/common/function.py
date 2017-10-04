def getText(element):
    if element!=None:
        txt=element.get_text()
        if str(txt).strip()=="---":
            txt="0"
        return txt
    return ""