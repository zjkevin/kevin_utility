from bottle import response
from bottle import request

def allow_cross_domain(fn):  
    def _enable_cors(*args, **kwargs):  
        #set cross headers  
        response.headers['Access-Control-Allow-Origin'] = '*'  
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS'  
        allow_headers = 'Referer, Accept, Origin, User-Agent'  
        response.headers['Access-Control-Allow-Headers'] = allow_headers       
        if request.method != 'OPTIONS':
            # actual request; reply with the actual response  
            return fn(*args, **kwargs)      
    return _enable_cors