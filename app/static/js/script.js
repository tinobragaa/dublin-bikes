// Get the elements.
const hamburgerMenu = document.getElementById('hamburger-menu');
const loginIcon = document.getElementById('login-icon');
const navBar = document.querySelector('.nav-bar');
const navLinks = document.getElementById('nav-links');
const hamburgerLinks = document.getElementById('hamburger-links');
const loginLinks = document.getElementById('login-links');
const allLinks = document.querySelectorAll('.nav-links-container a');

// This variable tracks which menu is currently open.
let currentMenu = null;

// Function to open the nav with a specific menu type.
function openMenu(menuType) {
  navBar.classList.add('expanded'); 
  navLinks.classList.add('show');

  if (menuType === "hamburger") {
    hamburgerLinks.style.display = 'flex';
    loginLinks.style.display = 'none';
  } else if (menuType === "login") {
    loginLinks.style.display = 'flex';
    hamburgerLinks.style.display = 'none';
  }
  currentMenu = menuType;
}

// Function to close the nav.
function closeMenu() {
  navBar.classList.remove('expanded');
  navLinks.classList.remove('show');
  currentMenu = null;
}

// Toggle function that checks current state and acts accordingly.
function toggleMenu(menuType) {
  if (!navBar.classList.contains('expanded')) {
    openMenu(menuType);
  } else {
    if (currentMenu === menuType) {
      closeMenu();
    } else {
      if (menuType === "hamburger") {
        hamburgerLinks.style.display = 'flex';
        loginLinks.style.display = 'none';
      } else if (menuType === "login") {
        loginLinks.style.display = 'flex';
        hamburgerLinks.style.display = 'none';
      }
      currentMenu = menuType;
    }
  }
}

// Attach event listeners to the icons.
hamburgerMenu.addEventListener('click', () => {
  toggleMenu("hamburger");
});

loginIcon.addEventListener('click', () => {
  toggleMenu("login");
});

// Close the nav when linked is clicke.
allLinks.forEach(link => {
    link.addEventListener('click', () => {
        closeMenu();
    });
});