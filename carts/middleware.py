from .models import Cart

class EnsureCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.save()

        session_key = request.session.session_key
        
        if not request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            cart, created = Cart.objects.get_or_create(session_key=session_key, is_active = True)

        request.cart = cart

        return self.get_response(request)