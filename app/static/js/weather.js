const weatherOverlay = document.getElementById('weather-overlay');
const currentTempEl = document.getElementById('current-temp');
const forecastEl = document.getElementById('forecast');
const refreshButton = document.getElementById('weather-refresh');
const weatherIconEl = document.getElementById('weather-icon'); // <-- Make sure this exists in your HTML

// Fetch weather data for Dublin
async function fetchWeather() {
    try {
        const response = await fetch('https://api.open-meteo.com/v1/forecast?latitude=53.3498&longitude=-6.2603&current_weather=true&daily=temperature_2m_min,temperature_2m_max&timezone=Europe%2FDublin');
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();

        // Current weather
        const currentTemp = data.current_weather.temperature;
        const weatherCode = data.current_weather.weathercode;

        // Get icon + color visuals
        const visuals = getWeatherVisuals(weatherCode, currentTemp);

        // Apply visuals
        if (weatherIconEl) weatherIconEl.textContent = visuals.icon;
        if (weatherOverlay) weatherOverlay.style.background = visuals.bgColor;

        currentTempEl.textContent = `Current Temp: ${currentTemp}°C, ${mapWeatherCode(weatherCode)}`;

        // Simple forecast
        const todayMin = data.daily.temperature_2m_min[0];
        const todayMax = data.daily.temperature_2m_max[0];
        forecastEl.textContent = `Today: ${todayMin}°C - ${todayMax}°C`;

    } catch (error) {
        console.error('Weather fetch failed:', error);
        currentTempEl.textContent = 'Unable to load weather.';
        forecastEl.textContent = '';
    }
}

// Map weather code to human-readable text
function mapWeatherCode(code) {
    const weatherCodes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        80: 'Rain showers',
        95: 'Thunderstorm',
        99: 'Severe thunderstorm'
    };

    return weatherCodes[code] || 'Unknown';
}

// Map weather + temperature to icons and background color
function getWeatherVisuals(code, temp) {
    let icon = '❔';
    let bgColor = '#1e1e2f'; // default dark

    if (code === 0) {
        icon = '☀️';
        bgColor = temp > 25 ? '#FDB813' : '#FFD166';
    } else if ([1, 2, 3].includes(code)) {
        icon = '⛅';
        bgColor = '#B0BEC5';
    } else if ([45, 48].includes(code)) {
        icon = '🌫️';
        bgColor = '#90A4AE';
    } else if ([51, 53, 55, 61, 63, 65, 80].includes(code)) {
        icon = '🌧️';
        bgColor = '#4A90E2';
    } else if ([71, 73, 75].includes(code)) {
        icon = '❄️';
        bgColor = '#E0F7FA';
    } else if (code >= 95) {
        icon = '⛈️';
        bgColor = '#6C63FF';
    }

    return { icon, bgColor };
}

// Attach refresh button listener
if (refreshButton) {
    refreshButton.addEventListener('click', () => {
        currentTempEl.textContent = 'Refreshing...';
        forecastEl.textContent = '';
        fetchWeather();
    });
}

// Load weather on page load
fetchWeather();
