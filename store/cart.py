from .models import Cart, CartItem, Product


class CartHelper:
    """
    Session-based cart helper.
    - Logged-in user → Cart tied to user (DB)
    - Guest → Cart tied to session_key (DB)
    """

    def __init__(self, request):
        self.request = request
        self.session = request.session

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not self.session.session_key:
                self.session.create()
            session_key = self.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)

        self.cart = cart

    # ─────────────────────────────────────
    # ADD
    # ─────────────────────────────────────
    def add(self, product, quantity=1):
        """Add product to cart or increase quantity."""
        if quantity < 1:
            quantity = 1

        # Stock limit
        if quantity > product.stock:
            quantity = product.stock

        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            new_qty = item.quantity + quantity
            if new_qty > product.stock:
                new_qty = product.stock
            item.quantity = new_qty
            item.save()

        return item

    # ─────────────────────────────────────
    # UPDATE QUANTITY
    # ─────────────────────────────────────
    def update(self, product_id, quantity):
        """Set exact quantity for a cart item."""
        try:
            item = CartItem.objects.get(cart=self.cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return None

        quantity = int(quantity)

        if quantity < 1:
            item.delete()
            return None

        if quantity > item.product.stock:
            quantity = item.product.stock

        item.quantity = quantity
        item.save()
        return item

    # ─────────────────────────────────────
    # REMOVE
    # ─────────────────────────────────────
    def remove(self, product_id):
        """Remove product from cart."""
        CartItem.objects.filter(cart=self.cart, product_id=product_id).delete()

    # ─────────────────────────────────────
    # CLEAR
    # ─────────────────────────────────────
    def clear(self):
        """Remove all items from cart."""
        self.cart.items.all().delete()

    # ─────────────────────────────────────
    # READ
    # ─────────────────────────────────────
    def get_items(self):
        return self.cart.items.select_related('product').all()

    def total_items(self):
        return sum(item.quantity for item in self.cart.items.all())

    def subtotal(self):
        return sum(item.total_price for item in self.cart.items.all())

    def is_empty(self):
        return not self.cart.items.exists()