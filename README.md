# 🛒 MyStore — Django E-Commerce Platform

A full-featured e-commerce web application built with **Django**, **HTML/CSS/JavaScript**, and **SQLite** — created as **Task 1** for the **CodeAlpha Full Stack Development Internship**.

---

## 📌 Project Overview

MyStore is a production-ready e-commerce store with complete shopping workflow: product browsing, cart management, secure checkout, order tracking, product reviews, and a custom admin dashboard.

**Live Demo:** _coming soon after deployment_

---

## ✨ Features

### 🛍️ Storefront
- **Product Listings** with search & category filters
- **Product Detail Pages** with related products
- **Product Reviews & Ratings** (1-5 stars + comments)
- **Responsive Design** (mobile-first)

### 🛒 Shopping Cart
- Session-based cart (guest + logged-in users)
- Add / update / remove items
- Stock validation & limits
- Free shipping on orders above ₹999

### 👤 User System
- **Registration** with validation
- **Login / Logout**
- **User Profile** (edit info, change password)
- **Guest cart merge** on login

### 📦 Order Management
- **Checkout** with shipping form
- **Order Success** page
- **Order History** with status tracking
- **Stock auto-deduction**

### 🎛️ Admin Dashboard (Jazzmin)
- Custom branded admin panel
- Product management with thumbnails
- Order status workflow (Pending → Processing → Shipped → Delivered)
- Bulk actions, filters, and search
- Review moderation

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 5.x |
| **Database** | SQLite (dev) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Admin Theme** | Django Jazzmin |
| **Auth** | Django built-in + custom Profile |
| **Server** | Gunicorn (production ready) |

---

## 📋 Task Requirements — Coverage

**CodeAlpha Task 1:** Simple E-Commerce Store

| Requirement | Status |
|-------------|--------|
| Product Listings | ✅ |
| Shopping Cart | ✅ |
| Product Details Page | ✅ |
| Order Processing | ✅ |
| User Registration/Login | ✅ |
| Database (products, users, orders) | ✅ |

**Bonus features:** Reviews, Profile, Admin dashboard, Order history, Search, Category filters, Stock management.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/praveenraj444/CodeAlpha_MyStore.git
cd CodeAlpha_MyStore

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Seed sample products (downloads images automatically)
python manage.py seed_products --clear

# 6. Create superuser (admin)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```
> 💡 **Note:** Product images are downloaded automatically when you run `seed_products`. Media files are not committed to the repository to keep the repo size small.


**Visit:** http://127.0.0.1:8000/

**Admin:** http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
CodeAlpha_MyStore/
├── manage.py
├── requirements.txt
├── .gitignore
├── avengers_cart/           # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/                   # Main app
    ├── models.py            # Category, Product, Cart, CartItem, Order, OrderItem, Review, Profile
    ├── views.py             # 15+ views
    ├── urls.py              # URL routing
    ├── admin.py             # Customized admin
    ├── forms.py             # RegisterForm, LoginForm, CheckoutForm, ReviewForm, etc.
    ├── cart.py              # CartHelper class
    ├── signals.py           # Auto Profile creation
    ├── context_processors.py# Cart count for navbar
    ├── management/
    │   └── commands/
    │       └── seed_products.py
    ├── templates/store/     # 13 HTML templates
    └── static/store/        # CSS + JS
```

---

## 🗄️ Database Models

| Model | Purpose |
|-------|---------|
| `Category` | Product categories |
| `Product` | Products (name, price, image, stock) |
| `Cart` | Shopping cart (user or guest session) |
| `CartItem` | Items inside a cart |
| `Order` | Placed orders with status |
| `OrderItem` | Products inside each order |
| `Review` | Product reviews (rating + comment) |
| `Profile` | Extended user info (phone, address) |

---

## 🎨 Pages

1. **Home** — Product listing with search & filters
2. **Product Detail** — Full info + reviews + related products
3. **Shopping Cart** — Items, quantities, totals
4. **Register** — New user signup
5. **Login** — User authentication
6. **Checkout** — Shipping details + order placement
7. **Order Success** — Confirmation with order summary
8. **Order History** — User's past orders
9. **User Profile** — Account info + edit
10. **Change Password** — Secure password update

---

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing (Django default)
- Login required for checkout, profile, orders
- User-scoped order access (users see only their orders)
- SQL injection safe (Django ORM)
- XSS protection (template auto-escaping)

---

## 📸 Screenshots

_Screenshots coming soon — will be added after deployment._

**Planned:**
- Home page (product grid)
- Product detail (with reviews)
- Shopping cart
- Checkout flow
- Admin dashboard (Jazzmin)
- User profile

---

## 🚢 Deployment

This project is designed for easy deployment to:
- **Render** (recommended — free tier)
- **Railway**
- **PythonAnywhere**
- **Heroku**

Production-ready with:
- `gunicorn` WSGI server
- `whitenoise` for static files
- `dj-database-url` for PostgreSQL
- Environment variables via `.env`

---

## 👨‍💻 Author

**Praveen Raj**
- GitHub: [@praveenraj444](https://github.com/praveenraj444)
- LinkedIn: linkedin.com/in/praveenraj-m-432aa2386
- Email: (praveenrajm2021@gmail.com)

---

## 🏢 Internship

**CodeAlpha — Full Stack Development Internship**
- Task 1: Simple E-Commerce Store
- Company: [CodeAlpha](https://www.codealpha.tech)
- Contact: services@codealpha.tech

---

## 📄 License

This project is created for educational purposes as part of the CodeAlpha Internship Program.

---

## 🙏 Acknowledgements

- **Django** — Web framework
- **Jazzmin** — Admin theme
- **Font Awesome** — Icons
- **CodeAlpha** — Internship opportunity

---

⭐ **If you found this project helpful, please give it a star!**
