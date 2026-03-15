const categoryNames = document.querySelectorAll('.category-name');

categoryNames.forEach(category => {
  category.addEventListener('mouseover', () => {
    category.style.fontSize = '1.7em'; // 
  });
  
  category.addEventListener('mouseout', () => {
    category.style.fontSize = '1.5em'; 
  });
});

function navigateToCategory(category) {
  window.location.href = `/products/${category}`;
}