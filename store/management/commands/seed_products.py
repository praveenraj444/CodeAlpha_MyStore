from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product


CATEGORIES = [
    "T-Shirts",
    "Shirts",
    "Chains",
    "Watches",
    "Shoes",
    "Bags",
]


PRODUCTS = [
    # ── T-Shirts ───────────────────────────
    {
        "category": "T-Shirts",
        "name": "Classic White Cotton T-Shirt",
        "description": "Premium 100% cotton crew-neck t-shirt. Breathable, soft, and perfect for everyday wear.",
        "price": "499.00",
        "stock": 50,
    },
    {
        "category": "T-Shirts",
        "name": "Black Graphic Print T-Shirt",
        "description": "Trendy black t-shirt with minimal graphic print. Regular fit, bio-washed fabric.",
        "price": "599.00",
        "stock": 40,
    },
    {
        "category": "T-Shirts",
        "name": "Navy Blue Polo T-Shirt",
        "description": "Smart casual polo t-shirt with collar. Perfect for office and outings.",
        "price": "799.00",
        "stock": 30,
    },
    {
        "category": "T-Shirts",
        "name": "Grey Melange Round Neck",
        "description": "Soft grey melange t-shirt. Comfortable all-day wear. Available in all sizes.",
        "price": "549.00",
        "stock": 35,
    },

    # ── Shirts ─────────────────────────────
    {
        "category": "Shirts",
        "name": "White Formal Shirt",
        "description": "Classic white formal shirt with slim fit. Wrinkle-resistant fabric. Ideal for office.",
        "price": "1299.00",
        "stock": 25,
    },
    {
        "category": "Shirts",
        "name": "Blue Checked Casual Shirt",
        "description": "Blue and white checked casual shirt. 100% cotton, full sleeves, button-down collar.",
        "price": "1199.00",
        "stock": 22,
    },
    {
        "category": "Shirts",
        "name": "Black Denim Shirt",
        "description": "Rugged black denim shirt. Durable stitching, dual chest pockets. Stylish and tough.",
        "price": "1499.00",
        "stock": 18,
    },
    {
        "category": "Shirts",
        "name": "Olive Green Linen Shirt",
        "description": "Breathable linen shirt in olive green. Perfect for summer. Half sleeves.",
        "price": "1399.00",
        "stock": 20,
    },

    # ── Chains ─────────────────────────────
    {
        "category": "Chains",
        "name": "Gold-Plated Cuban Chain",
        "description": "Stainless steel chain with gold plating. 20-inch length. Tarnish-resistant.",
        "price": "899.00",
        "stock": 30,
    },
    {
        "category": "Chains",
        "name": "Silver Figaro Chain Necklace",
        "description": "925 sterling silver Figaro chain. 22-inch length. Elegant and timeless.",
        "price": "2499.00",
        "stock": 15,
    },
    {
        "category": "Chains",
        "name": "Black Matte Rope Chain",
        "description": "Matte black stainless steel rope chain. Modern design, durable build.",
        "price": "699.00",
        "stock": 40,
    },
    {
        "category": "Chains",
        "name": "Rose Gold Pendant Chain",
        "description": "Rose gold chain with geometric pendant. Perfect gift for someone special.",
        "price": "1199.00",
        "stock": 25,
    },

    # ── Watches ────────────────────────────
    {
        "category": "Watches",
        "name": "Classic Analog Leather Watch",
        "description": "Brown leather strap with minimalist dial. Water-resistant. Quartz movement.",
        "price": "1999.00",
        "stock": 20,
    },
    {
        "category": "Watches",
        "name": "Digital Sports Watch",
        "description": "Shock-resistant digital watch with stopwatch, alarm, and backlight. Water-resistant 50m.",
        "price": "1499.00",
        "stock": 28,
    },
    {
        "category": "Watches",
        "name": "Stainless Steel Chronograph",
        "description": "Premium chronograph watch with stainless steel strap. Date display. 3 sub-dials.",
        "price": "3999.00",
        "stock": 12,
    },
    {
        "category": "Watches",
        "name": "Smart Fitness Watch",
        "description": "Fitness tracker with heart rate monitor, step counter, and sleep tracking. 7-day battery.",
        "price": "2999.00",
        "stock": 18,
    },

    # ── Shoes ──────────────────────────────
    {
        "category": "Shoes",
        "name": "White Running Sneakers",
        "description": "Lightweight running shoes with cushioned sole. Breathable mesh upper. Unisex.",
        "price": "2499.00",
        "stock": 22,
    },
    {
        "category": "Shoes",
        "name": "Brown Leather Formal Shoes",
        "description": "Genuine leather formal shoes with lace-up. Classic Oxford style. Durable sole.",
        "price": "2999.00",
        "stock": 15,
    },
    {
        "category": "Shoes",
        "name": "Black Canvas Sneakers",
        "description": "Casual black canvas shoes. Vulcanized rubber sole. Perfect for daily wear.",
        "price": "1299.00",
        "stock": 35,
    },
    {
        "category": "Shoes",
        "name": "Sports Running Shoes",
        "description": "Professional sports shoes with arch support. Anti-slip sole. Ideal for gym.",
        "price": "2199.00",
        "stock": 20,
    },

    # ── Bags ───────────────────────────────
    {
        "category": "Bags",
        "name": "Black Leather Laptop Bag",
        "description": "Premium leather laptop bag. Fits up to 15.6-inch laptops. Multiple compartments.",
        "price": "2499.00",
        "stock": 18,
    },
    {
        "category": "Bags",
        "name": "Canvas Casual Backpack",
        "description": "Durable canvas backpack with padded straps. Water-resistant. 25L capacity.",
        "price": "1499.00",
        "stock": 30,
    },
    {
        "category": "Bags",
        "name": "Travel Duffel Bag",
        "description": "Spacious travel duffel with shoe compartment. 40L capacity. Cabin-friendly.",
        "price": "1999.00",
        "stock": 15,
    },
    {
        "category": "Bags",
        "name": "Mini Crossbody Sling Bag",
        "description": "Compact sling bag for essentials. Adjustable strap. Lightweight and trendy.",
        "price": "899.00",
        "stock": 35,
    },
]


class Command(BaseCommand):
    help = "Seed database with sample e-commerce products"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing products and categories before seeding',
        )

    def handle(self, *args, **options):
        # ── Optionally clear old data ──
        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️  Clearing old data...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Old data cleared'))

        # ── Create categories ──
        self.stdout.write(self.style.MIGRATE_HEADING('\n📁 Creating categories...'))
        category_map = {}
        for name in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name}
            )
            category_map[name] = cat
            status = '✨ Created' if created else '⏭️  Exists'
            self.stdout.write(f'  {status}: {name}')

        # ── Create products ──
        self.stdout.write(self.style.MIGRATE_HEADING('\n🛒 Creating products...'))
        created_count = 0
        skipped_count = 0

        for data in PRODUCTS:
            category = category_map.get(data['category'])
            slug = slugify(data['name'])

            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'price': data['price'],
                    'stock': data['stock'],
                    'category': category,
                    'available': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✨ {product.name}'))
            else:
                skipped_count += 1
                self.stdout.write(f'  ⏭️  Skipped: {product.name}')

        # ── Summary ──
        self.stdout.write(self.style.MIGRATE_HEADING('\n📊 Summary'))
        self.stdout.write(f'  Categories : {Category.objects.count()}')
        self.stdout.write(f'  Products   : {Product.objects.count()}')
        self.stdout.write(self.style.SUCCESS(f'  Created    : {created_count}'))
        self.stdout.write(f'  Skipped    : {skipped_count}')
        self.stdout.write(self.style.SUCCESS('\n🎉 Seeding complete!\n'))