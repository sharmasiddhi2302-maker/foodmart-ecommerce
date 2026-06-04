// ============================
// PAGE LOAD
// ============================
document.addEventListener('DOMContentLoaded', function () {

    // Auto-hide alerts
    document.querySelectorAll('.alert').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 3000);
    });

    // Hide message container
    const container = document.getElementById('message-container');
    if (container) {
        setTimeout(() => {
            container.style.opacity = "0";
            setTimeout(() => container.remove(), 500);
        }, 5000);
    }
});


// ============================
// ADD TO CART
// ============================
function addToCart(productId) {
    const container = document.getElementById(`cart-action-${productId}`);
    if (!container) return;

    const btn = container.querySelector("button");
    if (!btn || btn.disabled) return;

    btn.disabled = true;
    btn.innerText = "Adding...";

    fetch(`/add-to-cart/${productId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {

        updateCartUI(productId, data.quantity);

        // cart count update
        const cartCount = document.querySelector(".cart-count");
        if (cartCount && data.cart_count !== undefined) {
            cartCount.innerText = data.cart_count;
        }

        btn.disabled = false;
        btn.innerText = "ADD";
    })
    .catch(() => {
        btn.disabled = false;
        btn.innerText = "ADD";
    });
}


// ============================
// UPDATE CART UI
// ============================
function updateCartUI(productId, qty) {
    const container = document.getElementById(`cart-action-${productId}`);
    if (!container) return;

    if (qty <= 0) {
        container.innerHTML = `
            <button onclick="addToCart('${productId}')" class="add-btn">ADD</button>
        `;
        return;
    }

    container.innerHTML = `
        <div class="qty-box">
            <button onclick="updateQty('${productId}', -1)">-</button>
            <span>${qty}</span>
            <button onclick="updateQty('${productId}', 1)">+</button>
        </div>
    `;
}


// ============================
// UPDATE QUANTITY
// ============================
function updateQty(productId, actionType) {

    let action = actionType === 1 ? "increase" : "decrease";

    fetch(`/update-cart-ajax/${productId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ action: action })
    })
    .then(res => res.json())
    .then(data => {

        // Product page update
        updateCartUI(productId, data.quantity);

        // Cart page update
        const qtyElement = document.getElementById(`qty-${productId}`);
        const row = document.getElementById(`row-${productId}`);
        const totalElement = document.getElementById(`total-${productId}`);

        if (qtyElement) qtyElement.innerText = data.quantity;

        if (row && data.quantity <= 0) row.remove();

        if (totalElement && data.item_total !== undefined) {
            totalElement.innerText = "₹" + data.item_total;
        }

        // cart count
        const cartCount = document.querySelector(".cart-count");
        if (cartCount && data.cart_count !== undefined) {
            cartCount.innerText = data.cart_count;
        }
    });
}


// ============================
// CSRF TOKEN
// ============================
function getCSRFToken() {
    const cookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

