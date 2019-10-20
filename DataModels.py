import sys

class AppResponse:
    def __init__(self, success = False, code = '', message = '', data = None):
        self.success = success
        self.code = code
        self.message = message
        self.data = None
    
    def serialize(self):
        return {
            'success': self.success, 
            'code': self.code,
            'message': self.message,
            'data': self.data
        }

class CaptchaImage:
    def __init__(self, id, url, selected = False):
        self.id = 'captcha-img-'+str(id)
        self.url = url
        self.selected = False
    
    def serialize(self):
        return {
            'id': self.id, 
            'url': self.url,
            'selected': self.selected
        }

class ClarifaiRequest:
    def __init__(self):
        self.inputs = []
    def serialize(self):
        return{
            'inputs': self.inputs
        }