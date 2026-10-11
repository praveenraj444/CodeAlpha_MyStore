from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import StyledPasswordChangeForm

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # ── Cart ──
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ── Auth ──
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── Password Change ──
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='store/password_change.html',
        form_class=StyledPasswordChangeForm,
        success_url='/profile/'
    ), name='password_change'),

    # ── Checkout ──
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.checkout_success, name='checkout_success'),

    # ── Orders ──
    path('my-orders/', views.order_history, name='order_history'),
    path('my-orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # ── Reviews ──
    path('product/<slug:slug>/review/', views.submit_review, name='submit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    # ── Profile ──
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]