document.addEventListener("DOMContentLoaded", () => {
  const productsContainer = document.getElementById("products-container");
  const cartIcon = document.getElementById('cart-icon');
  const cartCount = document.getElementById('cart-count');
  const cartIconContainer = document.getElementById('cart-icon-container');
  const productModal = document.getElementById('productModal');
  const productName = document.getElementById('productName');
  const productPrice = document.getElementById('productPrice');
  const productRating = document.getElementById('productRating');
  const productDetails = document.getElementById('productDetails');

  // Retrieve cart data from localStorage
  let cart = JSON.parse(localStorage.getItem('cart')) || [];

  // Debug - print current cart contents on page load
  console.log("Initial cart:", JSON.stringify(cart, null, 2));

  // Update the cart count
  updateCartCount();

  // Listen for storage changes (when cart is updated from other pages)
  window.addEventListener('storage', function(event) {
    if (event.key === 'cart') {
      cart = JSON.parse(event.newValue) || [];
      updateCartCount();
    }
  });

  // Helper function to get user ID - implement based on how your auth system works
  function getUserId() {
    // This could be from a session cookie, localStorage, or other auth mechanism
    // For example:
    return localStorage.getItem('user_id') || localStorage.getItem('userId') || 1; // Default to 1 for testing
  }

  // Listen for clicks on the product container
  productsContainer.addEventListener('click', (event) => {
    const productCard = event.target.closest('.product-card');

    if (productCard) {
      // Handle Add to Cart button clicks separately
      if (event.target.classList.contains('add-to-cart-btn')) {
        event.stopPropagation(); // Prevent the click from triggering the modal logic
        const productId = productCard.getAttribute('data-id');
        const name = productCard.getAttribute('data-name');
        const price = productCard.getAttribute('data-price');
        const category = productCard.getAttribute('data-category');

        console.log(`Adding product - ID: ${productId} (${typeof productId}), Name: ${name}, Category: ${category}`);
        
        // Check if product ID is missing or empty
        if (!productId || productId.trim() === '') {
          console.error('ERROR: Empty or missing product ID!', productCard);
          alert('This product has an invalid ID. Please notify the administrator.');
          return;
        }
        
        console.log("Current cart contents:", JSON.stringify(cart, null, 2));

        // Check if the cart has reached the maximum limit (20 items)
        if (cart.length >= 20) {
          alert("You can only add up to 20 items to the cart.");
          return;
        }

        // For fashion items, prompt for size selection
        let size = null;
        if (category === 'fashion') {
          size = prompt("Please select a size (S, M, L, XL):");
          if (!size || !['S', 'M', 'L', 'XL'].includes(size.toUpperCase())) {
            alert("Invalid size selected. Please try again.");
            return;
          }
          size = size.toUpperCase();
        }

        // Convert IDs to strings for consistent comparison
        const productIdStr = String(productId);
        
        // Check if the product is already in the cart (with the EXACT same ID and size)
        const isProductInCart = cart.some(item => {
          const itemIdStr = String(item.id);
          console.log(`Comparing: Cart item ID ${itemIdStr} (${typeof item.id}) with product ID ${productIdStr} (${typeof productId})`);
          console.log(`Item size: ${item.size}, New size: ${size}`);
          
          if (category === 'fashion') {
            return itemIdStr === productIdStr && item.size === size;
          }
          return itemIdStr === productIdStr;
        });

        if (isProductInCart) {
          // Show a simple message instead of asking to increase quantity
          alert("This product is already in your cart.");
          return;
        }

        // Add product to the cart
        addToCart(productId, name, price, size);
        return;
      }

      // Handle product modal opening for the card or image click
      const name = productCard.getAttribute('data-name');
      const price = productCard.getAttribute('data-price');
      const rating = productCard.getAttribute('data-rating');
      const details = productCard.getAttribute('data-details');

      if (event.target.tagName === 'IMG' || event.target.closest('.product-card')) {
        showProductDetails(name, price, rating, details);
      }
    }
  });

  // Function to add product to cart
  function addToCart(id, name, price, size = null) {
    console.log(`Adding to cart - ID: ${id}, Name: ${name}, Size: ${size}`);
    
    // Create product object
    const product = { 
      id: id, 
      name: name, 
      price: price, 
      size: size, 
      quantity: 1 
    };
    
    // Add product to the cart
    cart.push(product);

    // Save to localStorage
    saveCartToLocalStorage();
    
    // Update UI
    updateCartCount();
    animateCartIcon();
    
    console.log("Updated cart:", JSON.stringify(cart, null, 2));
    
    // Now also add to backend database
    const userId = getUserId();
    
    fetch('/api/carts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        Product_Id: id,
        User_Id: userId,
        Cart_Size: size,
        Product_Quantity: 1,
        Product_Price: price
      })
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
      if (status === 201 || status === 200) {
        console.log('Successfully added to backend cart:', body);
        // Store cart_id if provided in response
        if (body.Cart_Id) {
          product.cart_id = body.Cart_Id;
        }
        // Update the cart item in localStorage with cart_id
        const cartIndex = cart.findIndex(item => 
          String(item.id) === String(id) && item.size === size
        );
        if (cartIndex !== -1 && body.Cart_Id) {
          cart[cartIndex].cart_id = body.Cart_Id;
          saveCartToLocalStorage();
        }
      } else {
        console.error('Failed to add to backend cart:', body);
      }
    })
    .catch((error) => {
      console.error('Error adding to backend cart:', error);
    });
  }

  // Function to update the cart count
  function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
  }

  // Function to save cart to localStorage
  function saveCartToLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
  }

  // Function to add bounce animation to the cart icon
  function animateCartIcon() {
    cartIconContainer.classList.add('bounce');
    setTimeout(() => {
      cartIconContainer.classList.remove('bounce');
    }, 500);
  }

  // Show product details in the modal
  function showProductDetails(name, price, rating, details) {
    productName.textContent = name || 'No name available';
    productPrice.textContent = price ? `Price: ₹${price}` : 'No price available';
    productRating.textContent = rating ? `Rating: ${rating}☆` : 'No rating available';
    productDetails.textContent = details || 'No details available';

    if (details) {
      const detailsArray = details.split('\n');
      let formattedDetails = 'Details:<br>';
      detailsArray.forEach(detail => {
        formattedDetails += `<div style="text-align: center;">${detail.trim()}</div>`;
      });
      productDetails.innerHTML = formattedDetails;
    } else {
      productDetails.innerHTML = 'No details available';
    }

    productModal.style.display = 'block';
  }

  // Close modal
  function closeProductDetails() {
    productModal.style.display = 'none';
  }

  // Close modal when clicking on the close button
  const closeModalBtn = document.querySelector('.close-btn');
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeProductDetails);
  }

  // Redirect to cart when clicking the cart icon
  if (cartIcon) {
    cartIcon.addEventListener('click', function () {
      window.location.href = '/carts';
    });
  }

  // Redirect to cart when clicking the cart count
  if (cartCount) {
    cartCount.addEventListener('click', function () {
      window.location.href = '/carts';
    });
  }

  // Close modal when clicking outside of it
  window.addEventListener('click', function(event) {
    if (event.target === productModal) {
      closeProductDetails();
    }
  });

  // Sync cart with backend on page load
  function syncCartWithBackend() {
    const userId = getUserId();
    
    // Skip if no user is logged in
    if (!userId) return;
    
    fetch('/api/carts/sync', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
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
  
  // Initial sync with backend
  syncCartWithBackend();

  console.log("Products page loaded successfully!");
});