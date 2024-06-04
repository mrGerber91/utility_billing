class SecurityAndCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp = (
            "default-src 'self';"
            "script-src 'self' https://use.fontawesome.com;"
            "style-src 'self' https://cdnjs.cloudflare.com 'unsafe-inline';"
            "img-src 'self' https://s3.timeweb.cloud;"
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp
        response['X-Content-Type-Options'] = 'nosniff'
        response['Cache-Control'] = 'max-age=31536000, immutable'
        return response

