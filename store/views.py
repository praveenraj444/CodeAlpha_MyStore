from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from .models import Product, Category, Order, OrderItem, Review, Profile
from .cart import CartHelper
from .forms import RegisterForm, LoginForm, CheckoutForm, ReviewForm, UserForm, ProfileForm

# ═══════════════════════════════════════════
# HOME / PRODUCT LISTING
# ═══════════════════════════════════════════
def home(request):
    products = Product.objects.filter(available=True).select_related('category')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(name__icontains=query)

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'query': query,
    }
    return render(request, 'store/home.html', context)


# ═══════════════════════════════════════════
# PRODUCT DETAIL
# ═══════════════════════════════════════════
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    reviews = product.reviews.select_related('user').all()
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    review_form = ReviewForm()

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
    }
    return render(request, 'store/product_detail.html', context)


# ═══════════════════════════════════════════
# CART — VIEW
# ═══════════════════════════════════════════
def cart_view(request):
    cart = CartHelper(request)
    items = cart.get_items()

    context = {
        'items': items,
        'subtotal': cart.subtotal(),
        'total_items': cart.total_items(),
        'is_empty': cart.is_empty(),
    }
    return render(request, 'store/cart.html', context)


# ═══════════════════════════════════════════
# CART — ADD
# ═══════════════════════════════════════════
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock < 1:
        messages.error(request, f'"{product.name}" is out of stock.')
        return redirect('product_detail', slug=product.slug)

    quantity = int(request.POST.get('quantity', 1))

    cart = CartHelper(request)
    cart.add(product, quantity)

    messages.success(request, f'✅ "{product.name}" added to cart.')

    # If "buy now" → go to cart; else stay on product page
    if request.POST.get('buy_now'):
        return redirect('cart')
    return redirect('product_detail', slug=product.slug)


# ═══════════════════════════════════════════
# CART — UPDATE QUANTITY
# ═══════════════════════════════════════════
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        cart = CartHelper(request)
        cart.update(product_id, quantity)
        messages.success(request, '🔄 Cart updated.')
    return redirect('cart')


# ═══════════════════════════════════════════
# CART — REMOVE
# ═══════════════════════════════════════════
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = CartHelper(request)
    cart.remove(product_id)
    messages.success(request, f'🗑️ "{product.name}" removed from cart.')
    return redirect('cart')


# ═══════════════════════════════════════════
# REGISTER
# ═══════════════════════════════════════════
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            merge_guest_cart(request, user)
            messages.success(request, f'🎉 Welcome, {user.username}! Account created.')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


# ═══════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            merge_guest_cart(request, user)
            messages.success(request, f'👋 Welcome back, {user.username}!')

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'store/login.html', {'form': form})


# ═══════════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════════
def logout_view(request):
    logout(request)
    messages.info(request, '👋 Logged out successfully.')
    return redirect('home')

# ═══════════════════════════════════════════
# HELPER: Merge guest cart → user cart on login
# ═══════════════════════════════════════════
def merge_guest_cart(request, user):
    """
    Guest-ஆ இருக்கும்போது session-based cart-ல items இருந்தா,
    login ஆனபிறகு user-ஓட cart-க்கு move பண்ணு.
    """
    from .models import Cart, CartItem

    session_key = request.session.session_key
    if not session_key:
        return

    # Guest cart (session_key-based, no user)
    try:
        guest_cart = Cart.objects.get(session_key=session_key, user=None)
    except Cart.DoesNotExist:
        return

    if not guest_cart.items.exists():
        guest_cart.delete()
        return

    # User cart (create if needed)
    user_cart, _ = Cart.objects.get_or_create(user=user)

    # Move items
    for guest_item in guest_cart.items.all():
        existing = CartItem.objects.filter(
            cart=user_cart,
            product=guest_item.product
        ).first()

        if existing:
            existing.quantity += guest_item.quantity
            if existing.quantity > guest_item.product.stock:
                existing.quantity = guest_item.product.stock
            existing.save()
        else:
            CartItem.objects.create(
                cart=user_cart,
                product=guest_item.product,
                quantity=guest_item.quantity
            )

    # Delete guest cart
    guest_cart.delete()

    # ═══════════════════════════════════════════
# CHECKOUT
# ═══════════════════════════════════════════
@login_required
def checkout(request):
    cart = CartHelper(request)

    # ── Empty cart → home ──
    if cart.is_empty():
        messages.warning(request, '🛒 Cart is empty. Please add some products.')
        return redirect('home')

    subtotal = cart.subtotal()
    shipping = 0 if subtotal >= 999 else 99
    total = subtotal + shipping

    # ── Pre-fill from user ──
    initial = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    pincode=form.cleaned_data['pincode'],
                    total_amount=total,
                    status='pending',
                )

                # Create order items + reduce stock
                for item in cart.get_items():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        price=item.product.price,
                        quantity=item.quantity,
                    )

                    # Reduce stock
                    product = item.product
                    product.stock -= item.quantity
                    if product.stock <= 0:
                        product.stock = 0
                        product.available = False
                    product.save()

                # Clear cart
                cart.clear()

            messages.success(request, f'🎉 Order #{order.id} placed successfully!')
            return redirect('checkout_success', order_id=order.id)
        else:
            messages.error(request, 'Could not submit your review. Please check the form.')
    else:
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'items': cart.get_items(),
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'total_items': cart.total_items(),
    }
    return render(request, 'store/checkout.html', context)


# ═══════════════════════════════════════════
# CHECKOUT SUCCESS
# ═══════════════════════════════════════════
@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/checkout_success.html', {'order': order})

# ═══════════════════════════════════════════
# ORDER HISTORY
# ═══════════════════════════════════════════
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


# ═══════════════════════════════════════════
# ORDER DETAIL
# ═══════════════════════════════════════════
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

# ═══════════════════════════════════════════
# REVIEW — ADD / UPDATE
# ═══════════════════════════════════════════
@login_required
def submit_review(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        # Existing review-ஐ update, இல்லைனா create
        existing = Review.objects.filter(product=product, user=request.user).first()

        if existing:
            form = ReviewForm(request.POST, instance=existing)
            success_msg = '✅ Your review has been updated!'
        else:
            form = ReviewForm(request.POST)
            success_msg = '✅ Review submitted successfully. Thanks!'

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, success_msg)
        else:
            messages.error(request, 'Please fix the errors below.')

    return redirect('product_detail', slug=slug)


# ═══════════════════════════════════════════
# REVIEW — DELETE
# ═══════════════════════════════════════════
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, '🗑️ Review deleted successfully.')
    return redirect('product_detail', slug=product_slug)

# ═══════════════════════════════════════════
# USER PROFILE — VIEW
# ═══════════════════════════════════════════
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_orders = orders.count()
    total_spent = sum(order.total_amount for order in orders)

    context = {
        'profile': profile,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'recent_orders': orders[:3],
        'review_count': request.user.reviews.count(),
    }
    return render(request, 'store/profile.html', context)


# ═══════════════════════════════════════════
# USER PROFILE — EDIT
# ═══════════════════════════════════════════
@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'store/profile_edit.html', context)