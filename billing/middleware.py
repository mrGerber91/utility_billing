class SecurityAndCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Security-Policy'] = "default-src 'self'; frame-ancestors 'none';"
        response['X-Frame-Options'] = 'DENY'
        response['Cache-Control'] = 'max-age=31536000, immutable'
        return response
