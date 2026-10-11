from .cart import CartHelper


def cart_counter(request):
    try:
        cart = CartHelper(request)
        count = cart.total_items()
    except Exception:
        count = 0

    return {
        'cart_count': count,
    }