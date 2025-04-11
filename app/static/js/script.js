// NAVIGATION MENU LOGIC
const hamburgerMenu = document.getElementById('hamburger-menu');
const loginIcon = document.getElementById('login-icon');
const navBar = document.querySelector('.nav-bar');
const navLinks = document.getElementById('nav-links');
const hamburgerLinks = document.getElementById('hamburger-links');
const loginLinks = document.getElementById('login-links');
const allLinks = document.querySelectorAll('.nav-links-container a');

let currentMenu = null;

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

function closeMenu() {
  navBar.classList.remove('expanded');
  navLinks.classList.remove('show');
  currentMenu = null;
}

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

hamburgerMenu.addEventListener('click', () => toggleMenu("hamburger"));
loginIcon.addEventListener('click', () => toggleMenu("login"));

allLinks.forEach(link => {
  link.addEventListener('click', () => closeMenu());
});


// LEAFLET MAP + JCDECAUX INTEGRATION
const map = L.map('map').setView([53.3498, -6.2603], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 🚲 JCDecaux API integration
const apiKey = 'c68dab54bda9ba1de22a1c7fc5d29ed1537e33ca'; // Replace with your real API key

fetch(`https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=${apiKey}`)
let allStations = [];
let allMarkers = [];

// Helper to clear current markers
function clearMarkers() {
    allMarkers.forEach(marker => map.removeLayer(marker));
    allMarkers = [];
}

// Render markers based on filter/search
function updateMarkers() {
    const query = searchInput.value.toLowerCase();
    const minBikes = parseInt(bikeFilter.value);
    bikeCountDisplay.textContent = minBikes;

    clearMarkers();

    allStations.forEach(station => {
        const name = station.name.toLowerCase();
        if (name.includes(query) && station.available_bikes >= minBikes) {
            const marker = L.marker([station.position.lat, station.position.lng]).addTo(map);
            marker.bindPopup(`
                <div style="min-width:180px">
                    <h5 style="margin: 0 0 4px;">${station.name}</h5>
                    <hr style="margin: 4px 0;">
                    <p style="margin: 0;"><strong>Bikes:</strong> ${station.available_bikes}</p>
                    <p style="margin: 0;"><strong>Stands:</strong> ${station.available_bike_stands}</p>
                </div>
            `);
            allMarkers.push(marker);
        }
    });
}

// Fetch station data and initialize
fetch(`https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=${apiKey}`)
  .then(response => response.json())
  .then(stations => {
    stations.forEach(station => {
      if (station.position) {
        const marker = L.marker([station.position.lat, station.position.lng]).addTo(map);
        marker.bindPopup(`
          <div style="min-width:180px">
              <h5 style="margin: 0 0 4px;">${station.name}</h5>
              <hr style="margin: 4px 0;">
              <p style="margin: 0;"><strong>Bikes:</strong> ${station.available_bikes}</p>
              <p style="margin: 0;"><strong>Stands:</strong> ${station.available_bike_stands}</p>
          </div>
        `);
      }
    });
  })
  .catch(err => console.error('JCDecaux fetch error:', err));

// Live update on user input
searchInput.addEventListener('input', updateMarkers);
bikeFilter.addEventListener('input', updateMarkers);
function getMarkerColor(bikesAvailable) {
  if (bikesAvailable === 0) return 'red';
  if (bikesAvailable <= 3) return 'orange';
  return 'green';
}
const icon = L.icon({
  iconUrl: `/static/icons/marker-${getMarkerColor(station.available_bikes)}.png`,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34]
});

const marker = L.marker([station.position.lat, station.position.lng], { icon }).addTo(map);
const searchInput = document.getElementById("search-bar");

searchInput.addEventListener("input", (e) => {
  const searchTerm = e.target.value.toLowerCase();
  markers.forEach(({ station, marker }) => {
    const isVisible = station.name.toLowerCase().includes(searchTerm);
    if (isVisible) {
      marker.addTo(map);
    } else {
      map.removeLayer(marker);
    }
  });
});
const filterCheckbox = document.getElementById("show-available-only");
filterCheckbox.addEventListener("change", (e) => {
  const showOnlyAvailable = e.target.checked;
  markers.forEach(({ station, marker }) => {
    const shouldShow = !showOnlyAvailable || station.available_bikes > 0;
    if (shouldShow) {
      marker.addTo(map);
    } else {
      map.removeLayer(marker);
    }
  });
});
setInterval(fetchStations, 60000); // Re-fetch data every 60 seconds
// Save
localStorage.setItem("showAvailableOnly", showOnlyAvailable);

// Load
const saved = localStorage.getItem("showAvailableOnly");
if (saved === "true") {
  filterCheckbox.checked = true;
}
