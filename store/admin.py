from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review

# ═══════════════════════════════════════════
# ADMIN SITE BRANDING
# ═══════════════════════════════════════════
admin.site.site_header = "My Store — Admin"
admin.site.site_title = "My Store Admin"
admin.site.index_title = "Welcome to My Store Dashboard"


# ═══════════════════════════════════════════
# CATEGORY
# ═══════════════════════════════════════════
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    readonly_fields = ('created_at',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


# ═══════════════════════════════════════════
# PRODUCT
# ═══════════════════════════════════════════
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail', 'name', 'category', 'price',
        'stock', 'available', 'created_at'
    )
    list_filter = ('available', 'category', 'created_at')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'preview_image')
    list_per_page = 20

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Image', {
            'fields': ('image', 'preview_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;border-radius:6px;object-fit:cover;" />',
                obj.image.url
            )
        return '📦'
    thumbnail.short_description = 'Image'

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:250px;border-radius:8px;" />',
                obj.image.url
            )
        return 'No image uploaded'
    preview_image.short_description = 'Preview'


# ═══════════════════════════════════════════
# CART
# ═══════════════════════════════════════════
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'item_count', 'created_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


# ═══════════════════════════════════════════
# ORDER
# ═══════════════════════════════════════════
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'total_price_display')
    can_delete = False

    def total_price_display(self, obj):
        try:
            return f"₹{obj.total_price}"
        except Exception:
            return "—"
    total_price_display.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'email', 'phone',
        'total_amount', 'status_badge', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'id')
    readonly_fields = ('user', 'total_amount', 'created_at')
    inlines = [OrderItemInline]
    list_per_page = 20

    fieldsets = (
        ('Customer', {
            'fields': ('user', 'full_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'pincode')
        }),
        ('Order Info', {
            'fields': ('total_amount', 'status', 'created_at')
        }),
    )

    actions = ['mark_processing', 'mark_shipped', 'mark_delivered', 'mark_cancelled']

    def status_badge(self, obj):
        colors = {
            'pending': '#92400e',
            'processing': '#1d4ed8',
            'shipped': '#4338ca',
            'delivered': '#16a34a',
            'cancelled': '#dc2626',
        }
        bg = {
            'pending': '#fef3c7',
            'processing': '#dbeafe',
            'shipped': '#e0e7ff',
            'delivered': '#dcfce7',
            'cancelled': '#fee2e2',
        }
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;text-transform:uppercase;">{}</span>',
            bg.get(obj.status, '#eee'),
            colors.get(obj.status, '#333'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='✅ Mark as Processing')
    def mark_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f'{queryset.count()} order(s) marked as Processing.')

    @admin.action(description='🚚 Mark as Shipped')
    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, f'{queryset.count()} order(s) marked as Shipped.')

    @admin.action(description='📬 Mark as Delivered')
    def mark_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f'{queryset.count()} order(s) marked as Delivered.')

    @admin.action(description='❌ Mark as Cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} order(s) marked as Cancelled.')


# ═══════════════════════════════════════════
# CART ITEM / ORDER ITEM (standalone)
# ═══════════════════════════════════════════
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at')
    search_fields = ('product__name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'price', 'quantity')
    search_fields = ('product_name', 'order__id')

    # ═══════════════════════════════════════════
# REVIEW
# ═══════════════════════════════════════════
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating_stars', 'short_comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

    fieldsets = (
        ('Review Info', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = 'Rating'

    def short_comment(self, obj):
        if obj.comment:
            return obj.comment[:60] + ('…' if len(obj.comment) > 60 else '')
        return '—'
    short_comment.short_description = 'Comment'