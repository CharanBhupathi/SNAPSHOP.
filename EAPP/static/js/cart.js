const cart = JSON.parse(localStorage.getItem('cart')) || [];
const cartItemsContainer = document.getElementById('cart-items');
const totalPriceElement = document.getElementById('total-price');
const cartContent = document.getElementById('cart-content');
const emptyCartMessage = document.getElementById('empty-cart-message');
const cartCountElement = document.getElementById('cart-count');

// 🔒 Get user ID
function getUserId() {
  return localStorage.getItem('user_id') || 1;
}

// ✅ Add to cart with check
function addToCart(product) {
  const userId = getUserId();

  fetch('/api/carts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      product_id: product.id,
      quantity: 1,
      size: product.size || 0,
      price: product.price
    })
  })
    .then(res => res.json().then(data => ({ status: res.status, body: data })))
    .then(({ status, body }) => {
      if (status === 409) {
        alert(body.message); // Already in cart
      } else if (status === 201) {
        alert(body.message); // Added
        // ✅ Only push to local cart if backend accepted it
        cart.push({ ...product, quantity: 1 });
        saveCartToLocalStorage();
        updateCartCount();
        populateCart();
      } else {
        alert("Unexpected error");
        console.error(body);
      }
    })
    .catch(err => {
      console.error('Error adding to backend:', err);
    });
}

function populateCart() {
  cartItemsContainer.innerHTML = '';
  let total = 0;

  if (cart.length === 0) {
    cartContent.style.display = 'none';
    emptyCartMessage.style.display = 'block';
    return;
  }

  cartContent.style.display = 'block';
  emptyCartMessage.style.display = 'none';

  cart.forEach((item, index) => {
    const li = document.createElement('li');
    li.style.position = 'relative';

    const sizeDisplay = item.size ? `<p><strong>Size:</strong> ${item.size}</p>` : '';

    li.innerHTML = `
      <button class="remove-btn" data-index="${index}" 
        style="position: absolute; top: 10px; right: 10px; background-color: transparent; border: none; font-size: 1.2rem; color: red; cursor: pointer;">
        X
      </button>
      <p><strong>Product:</strong> ${item.name}</p>
      <p><strong>Price:</strong> ₹${item.price}</p>
      ${sizeDisplay}
      <div class="quantity-selector">
        <label for="quantity-${index}">Quantity:</label>
        <input type="number" id="quantity-${index}" value="${item.quantity}" min="1" max="10">
      </div>
    `;

    cartItemsContainer.appendChild(li);
    total += parseFloat(item.price) * item.quantity;

    document.getElementById(`quantity-${index}`).addEventListener('change', function () {
      updateQuantity(index, this.value);
    });
  });

  totalPriceElement.textContent = total.toFixed(2);
  updateCartCount();

  document.querySelectorAll('.remove-btn').forEach(button => {
    button.addEventListener('click', function () {
      const index = this.getAttribute('data-index');
      removeProductFromCart(index);
    });
  });
}

function updateQuantity(index, quantity) {
  const item = cart[index];
  cart[index].quantity = parseInt(quantity);
  saveCartToLocalStorage();
  
  // If we have a cart_id from backend, update it directly
  // Otherwise, sync the entire cart
  if (item.cart_id) {
    fetch(`/api/carts/${item.cart_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Product_Quantity: parseInt(quantity)
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Quantity updated in backend:', data);
        populateCart();
      })
      .catch(error => {
        console.error('Error updating quantity in backend:', error);
        // Still sync the entire cart as fallback
        syncCartWithBackend();
        populateCart();
      });
  } else {
    syncCartWithBackend();
    populateCart();
  }
}

function removeProductFromCart(index) {
  const item = cart[index];
  const userId = getUserId();
  
  // Remove from local cart
  cart.splice(index, 1);
  saveCartToLocalStorage();
  
  // If we have a cart_id from backend, delete it from database
  // Otherwise, sync the entire cart
  if (item.cart_id) {
    fetch(`/api/carts/${item.cart_id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    })
      .then(response => response.json())
      .then(data => {
        console.log('Item removed from backend:', data);
        populateCart();
      })
      .catch(error => {
        console.error('Error removing item from backend:', error);
        // Still sync the entire cart as fallback
        syncCartWithBackend();
        populateCart();
      });
  } else {
    syncCartWithBackend();
    populateCart();
  }
}

function updateCartCount() {
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  if (cartCountElement) {
    cartCountElement.textContent = totalItems;
  }
}

function saveCartToLocalStorage() {
  localStorage.setItem('cart', JSON.stringify(cart));
}

// 🔄 Load cart from backend database
function loadCartFromBackend() {
  const userId = getUserId();
  if (!userId) return Promise.resolve();

  return fetch(`/api/users/${userId}/carts`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => response.json())
    .then(cartItems => {
      console.log('Cart loaded from backend:', cartItems);
      
      if (!cartItems || cartItems.length === 0) {
        return; // No items in database
      }

      // Fetch product details for each cart item
      const productPromises = cartItems.map(cartItem => 
        fetch(`/api/products/${cartItem.Product_Id}`)
          .then(res => res.json())
          .then(product => ({
            id: product.Product_Id,
            name: product.Product_Name,
            price: product.Product_Price,
            quantity: cartItem.Product_Quantity,
            size: cartItem.Cart_Size,
            cart_id: cartItem.Cart_Id
          }))
          .catch(err => {
            console.error(`Error fetching product ${cartItem.Product_Id}:`, err);
            return null;
          })
      );

      return Promise.all(productPromises).then(products => {
        // Filter out any null products (errors)
        const validProducts = products.filter(p => p !== null);
        
        if (validProducts.length > 0) {
          // Update cart with items from database
          cart.length = 0; // Clear existing cart
          cart.push(...validProducts);
          saveCartToLocalStorage();
          console.log('Cart populated from backend:', cart);
        }
      });
    })
    .catch(error => {
      console.error('Error loading cart from backend:', error);
    });
}

// 🔄 Sync local cart with backend
function syncCartWithBackend() {
  const userId = getUserId();
  if (!userId) return;

  fetch('/api/carts/sync', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      cart_items: cart
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Cart synced with backend:', data);
    })
    .catch(error => {
      console.error('Error syncing cart:', error);
    });
}

// 🧹 Clear Cart
document.getElementById('clear-cart-btn')?.addEventListener('click', () => {
  const userId = getUserId();
  if (!userId) {
    alert("User not logged in!");
    return;
  }

  fetch('/api/carts/sync', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      cart_items: [] // Empty it!
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Cart cleared from backend:", data);
      localStorage.removeItem('cart');
      cart.length = 0;
      populateCart();
    })
    .catch(error => {
      console.error("Error clearing backend cart:", error);
    });
});

document.getElementById('checkout-btn')?.addEventListener('click', () => {
  alert('Checkout functionality coming soon!');
});

document.addEventListener('DOMContentLoaded', function () {
  // First load cart from backend to ensure we have the latest data from database
  loadCartFromBackend().then(() => {
    // After loading from backend, populate the cart UI
    populateCart();
    // If we have items in localStorage that aren't in backend, sync them
    syncCartWithBackend();
  }).catch(() => {
    // If loading from backend fails, still show localStorage cart
    populateCart();
  });
});