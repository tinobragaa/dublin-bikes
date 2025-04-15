/* NAVIGATION MENU LOGIC */
const hamburgerMenu = document.getElementById('hamburger-menu');
const loginIcon = document.getElementById('login-icon');
const navBar = document.querySelector('.nav-bar');
const navLinks = document.getElementById('nav-links');
const hamburgerLinks = document.getElementById('hamburger-links');
const loginLinks = document.getElementById('login-links');
const allLinks = document.querySelectorAll('.nav-links-container a');

let currentMenu = null;
let sidebarTimeout = null;

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

/* LEAFLET MAP & JCDECAUX INTEGRATION */
const apiKey = 'c68dab54bda9ba1de22a1c7fc5d29ed1537e33ca';
const map = L.map('map').setView([53.3498, -6.2603], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let allStations = [];
let allMarkers = [];

const searchInput = document.getElementById('search-input');
const bikeFilter = document.getElementById('bike-filter');
const bikeCountDisplay = document.getElementById('bike-filter-display');

function clearMarkers() {
  allMarkers.forEach(marker => map.removeLayer(marker));
  allMarkers = [];
}

function updateSidebar(station) {
  document.getElementById('sidebar-station-name').textContent = station.name;
  document.getElementById('sidebar-bikes').textContent = station.available_bikes;
  document.getElementById('sidebar-stands').textContent = station.available_bike_stands;

  const now = new Date();
  const daysArr = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const dayName = daysArr[now.getDay()];
  const currentHour = now.getHours();
  const stationId = station.number;

  // Prediction API call
  fetch(`/predict_bikes?station_id=${stationId}&day=${encodeURIComponent(dayName)}&hour=${currentHour}`)
    .then(response => response.json())
    .then(data => {
      const predictionElement = document.getElementById('sidebar-prediction');
      const future = new Date();
      future.setHours(future.getHours() + 1);
      const timeFormatted = future.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      if (data.error) {
        predictionElement.textContent = `Predicted Bikes (for ${timeFormatted}): Error`;
      } else {
        predictionElement.textContent = `Predicted Bikes (for ${timeFormatted}): ${data.predicted_bikes}`;
      }
    })
    .catch(err => {
      console.error('Prediction API error:', err);
      const fallbackTime = new Date();
      fallbackTime.setHours(fallbackTime.getHours() + 1);
      const fallbackFormatted = fallbackTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      document.getElementById('sidebar-prediction').textContent = `Predicted Bikes (for ${fallbackFormatted}): Error`;
    });

  // Recommendations if bikes == 0
  if (station.available_bikes === 0) {
    fetch(`/recommend_stations?station_id=${stationId}&condition=need_bikes`)
      .then(response => response.json())
      .then(data => {
        let recContainer = document.getElementById("sidebar-recommendations");
        if (!recContainer) {
          recContainer = document.createElement("div");
          recContainer.id = "sidebar-recommendations";
          document.getElementById('station-sidebar').appendChild(recContainer);
        }
        if (data.error || !data.recommendations || data.recommendations.length === 0) {
          recContainer.innerHTML = "<p>No recommendations available.</p>";
        } else {
          let html = "<h6>Recommended Nearby Stations:</h6><ul>";
          data.recommendations.forEach(function(rec) {
            html += `<li>${rec.name} (${rec.distance_km} km) - Bikes: ${rec.available_bikes}</li>`;
          });
          html += "</ul>";
          recContainer.innerHTML = html;
        }
      })
      .catch(err => {
        console.error("Recommendation API error:", err);
      });
  } else {
    const recContainer = document.getElementById("sidebar-recommendations");
    if (recContainer) {
      recContainer.remove();
    }
  }

  // Open the sidebar
  document.getElementById('station-sidebar').style.right = '0';

  if (sidebarTimeout) {
    clearTimeout(sidebarTimeout);
  }

  sidebarTimeout = setTimeout(() => {
    closeSidebar();
  }, 3000);
}

function updateMarkers() {
  const query = searchInput ? searchInput.value.toLowerCase() : "";
  const minBikes = bikeFilter ? parseInt(bikeFilter.value) : 0;

  if (bikeCountDisplay) {
    bikeCountDisplay.textContent = "Min Bikes: " + minBikes;
  }

  clearMarkers();

  allStations.forEach(station => {
    const stationName = station.name.toLowerCase();
    if (stationName.includes(query) && station.available_bikes >= minBikes) {
      let marker = L.marker([station.position.lat, station.position.lng]).addTo(map);
      marker.bindPopup(`
        <div style="min-width:180px">
          <h5 style="margin: 0 0 4px;">${station.name}</h5>
          <hr style="margin: 4px 0;">
          <p style="margin: 0;"><strong>Bikes:</strong> ${station.available_bikes}</p>
          <p style="margin: 0;"><strong>Stands:</strong> ${station.available_bike_stands}</p>
        </div>
      `);
      marker.on('click', () => {
        updateSidebar(station);
      });
      allMarkers.push(marker);
    }
  });
}

function fetchStations() {
  fetch(`https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=${apiKey}`)
    .then(response => response.json())
    .then(stations => {
      allStations = stations;
      updateMarkers();
    })
    .catch(err => console.error('JCDecaux fetch error:', err));
}

fetchStations();
setInterval(fetchStations, 60000);

if (searchInput) {
  searchInput.addEventListener('input', updateMarkers);
}
if (bikeFilter) {
  bikeFilter.addEventListener('input', updateMarkers);
}

function closeSidebar() {
  document.getElementById('station-sidebar').style.right = '-320px';
}
