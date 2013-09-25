# To change this template, choose Tools | Templates
# and open the template in the editor.


def html_message(text, type="alert", width=0):
    """
        tipos de mensajes
        info
        success
        alert
        error
    """
    if width != 0:
         return "<div class=\"%s\" style=\"width:%\"> %s </div>" %(type, text, width)
    else:
        return "<div class=\"%s\" > %s </div>" %(type, text)


def strong(text):
    return "<strong>%s</strong>" %text


def custom_tag(name="p", atrr="", content="", end_tag=True):
    if end_tag:
        return "<%s %s>%s<%s/>" %(name, atrr, content, name)
    else:
        return "<%s %s />" %(name, atrr)