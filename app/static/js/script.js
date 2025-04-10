// Get the relevant elements.
const hamburgerMenu = document.getElementById('hamburger-menu');
const loginIcon = document.getElementById('login-icon');
const navBar = document.querySelector('.nav-bar');
const navLinks = document.getElementById('nav-links');
const hamburgerLinks = document.getElementById('hamburger-links');
const loginLinks = document.getElementById('login-links');

// Function to toggle the expanded state.
function toggleNav() {
  navBar.classList.toggle('expanded');
  navLinks.classList.toggle('show'); 
}

// Event listener for the hamburger menu.
hamburgerMenu.addEventListener('click', () => {
  hamburgerLinks.style.display = 'flex';
  loginLinks.style.display = 'none';
  toggleNav();
});

// Event listener for the login icon.
loginIcon.addEventListener('click', () => {
  loginLinks.style.display = 'flex';
  hamburgerLinks.style.display = 'none';
  toggleNav();
});
