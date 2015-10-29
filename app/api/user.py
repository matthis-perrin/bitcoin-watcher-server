from pyramid.response import Response

def register(request):
    return dict(method=request.method)
