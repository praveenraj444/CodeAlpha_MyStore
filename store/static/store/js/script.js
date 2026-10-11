// ═══════════════════════════════════════════
// Auto-hide Django messages after 4 seconds
// ═══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });
});


// ═══════════════════════════════════════════
// Quantity +/- buttons (used in product_detail & cart)
// ═══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function () {
    const qtyInput = document.getElementById('quantity');
    const btnMinus = document.getElementById('qty-minus');
    const btnPlus = document.getElementById('qty-plus');

    if (qtyInput && btnMinus && btnPlus) {
        btnMinus.addEventListener('click', function () {
            let current = parseInt(qtyInput.value) || 1;
            if (current > 1) {
                qtyInput.value = current - 1;
            }
        });

        btnPlus.addEventListener('click', function () {
            let current = parseInt(qtyInput.value) || 1;
            const max = parseInt(qtyInput.max) || 999;
            if (current < max) {
                qtyInput.value = current + 1;
            }
        });
    }
});


// ═══════════════════════════════════════════
// Console greeting (fun touch)
// ═══════════════════════════════════════════
console.log('%c🛒 Avengers Cart', 'color: #c8102e; font-size: 20px; font-weight: bold;');
console.log('%c"Whatever it takes."', 'color: #ffb400; font-style: italic;');

// ═══════════════════════════════════════════
// Navbar Dropdown (Mobile tap + outside click)
// ═══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggle = document.querySelector('.nav-dropdown-toggle');
    const dropdown = document.querySelector('.nav-dropdown');

    if (dropdownToggle && dropdown) {
        dropdownToggle.addEventListener('click', function (e) {
            e.preventDefault();
            dropdown.classList.toggle('open');
        });

        // Outside click → close
        document.addEventListener('click', function (e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('open');
            }
        });
    }
});