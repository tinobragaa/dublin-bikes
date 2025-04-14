# Dublin Bikes
(Developers: Valentino Braga and Charan Singu)

Dublin Bikes is a user-focused web application designed to help individuals locate shared bicycles across Dublin city.cAt its core, the application pulls live station data from the JCDecaux API to display bike availability and locations across the city. Each station is represented on an interactive map with pins that users can click to access detailed station information. To further enhance the experience, a machine learning component analyses historical weather and station usage data to forecast bike availability based on current conditions. This allows users to make better-informed decisions when planning their journeys.

The goal of the project is to merge functionality, usability, and predictive insight into a single platform that supports both locals and tourists navigating Dublin’s bike sharing system. 

![Website Mockup Image](/docs/features/dublinbikes-mockup.png)

[Live Website](http://16.170.206.160/)

## Table of Contents

## Features

- **Map**
<br>
The interactive map is a core feature of the application, dynamically rendered using data fetched from the JCDecaux API. This data includes real-time information about bike stations across Dublin, such as location, name, and current bike availability. Each station is represented by a clickable pin on the map. When a user clicks a pin, a sidebar opens displaying detailed station information along with a machine learning-based prediction of future bike availability. At the bottom of the map, users can also filter stations using two input fields: one for searching by station name and another for filtering by available bike quantity.

![screenshot](/docs/features/map-final.png)
![screenshot](/docs/features/prediction.png)
![screenshot](/docs/features/search-control.png)

- **Weather Box**
<br>
The weather box displays real-time weather information by integrating data from the OpenWeather API. It presents key details such as current conditions, temperature highs and lows, and a weather code (e.g., sunny, rainy) that reflects the forecast. To enhance the user experience, the component also includes a matching weather icon that visually represents the current conditions. This feature helps users make informed decisions about cycling based on the day’s weather outlook.
![screenshot](/docs/features/weather-box.png)

- **Navigation Bar**
<br>
The navigation bar is implemented with a modern, minimalist design, using icon based elements that expand on click through JavaScript interactivity. It features a translucent, glass aesthetic with a blur effect, allowing background colours to show through and enhancing visual depth. The bar is fixed to the top of the screen, ensuring persistent accessibility as users scroll through the page. This design choice prioritises usability and seamless navigation across the interface.

![screenshot](/docs/features/nav-bar.png)

- **Sign In Page**
<br>
The sign in page provides a straightforward interface for returning users to access their accounts. It maintains visual continuity with the rest of the application by retaining the navigation bar at the top and logo at the bottom. 
![screenshot](/docs/features/log-in-final.png)

- **Sign Up Page**
<br>
The sign up page provides a straightforward interface where users can create an account. It maintains visual continuity with the rest of the application by retaining the navigation bar at the top and logo at the bottom. 
![screenshot](/docs/features/sign-up-final.png)

## Mockups vs. Production

- **Homepage**
  - Mockup:
  ![screenshot](/docs/mockup/homepage-mockup.png)

  - Final:
      ![screenshot](/docs/features/dublinbikes-homepage.png)

- **Maps**
  - Mockup:
  ![screenshot](/docs/mockup/map-mockup.png)

  - Final:
      ![screenshot](/docs/features/map-final.png)

- **Sign In**
  - Mockup:
  ![screenshot](/docs/mockup/log-in-mockup.png)

  - Final:
      ![screenshot](/docs/features/log-in-final.png)

- **Sign Up**
  - Mockup:
  ![screenshot](/docs/mockup/sign-up-mockup.png)

  - Final:
      ![screenshot](/docs/features/sign-up-final.png)


## Technologies Used

### Languages and Frameworks

This project was created using the following languages and frameworks:

- [HTML](https://en.wikipedia.org/wiki/HTML) for structuring the web content.
- [CSS](https://en.wikipedia.org/wiki/CSS) for styling and layout.
  - [Bootstrap](https://getbootstrap.com/) for responsive design and prebuilt UI components.
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript) for interactivity across the site.
  - [Leaflet.js](https://leafletjs.com/) for rendering interactive maps.
- [Python](https://www.python.org/) for backend logic and machine learning integration.
  - [Flask](https://flask.palletsprojects.com/) as the Python web framework.

### Resources and Tools

The following resources and tools were used during development:

- [Visual Studio Code](https://code.visualstudio.com/) (VS Code) – Development environment.
- [Git](https://git-scm.com/) and [GitHub](https://github.com/) – For version control and collaboration.
- [JCDecaux API](https://developer.jcdecaux.com/) – Provides real-time data on Dublin’s bike stations.
- [OpenWeather API](https://openweathermap.org/api) – Used to retrieve real-time weather data and forecasts.
- [WhatsApp](https://www.whatsapp.com/), [Discord](https://discord.com/), [Zoom](https://zoom.us/) – Used for team communication.
- [Google Docs](https://docs.google.com/) – Used as a shared Task Tracker and for report collaboration.
- [Figma](https://www.figma.com/), [Canva](https://www.canva.com/), [Behance](https://www.behance.net/) – Used for UI mockups and design planning.
- [Google Fonts](https://fonts.google.com/) – Used for web typography.
- [Google Icons](https://fonts.google.com/icons) and [Font Awesome](https://fontawesome.com/) – Used for iconography across the interface.
- [HTML W3C Validator](https://validator.w3.org/) – Used to validate HTML markup.
- [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/) – Used to validate CSS.
- [Stack Overflow](https://stackoverflow.com/) – Consulted for solutions to development issues.
- [ChatGPT](https://chat.openai.com/) – Used to support project planning and technical problem-solving.

## Deployment

### EC2 Deployment

This project is built for easy deployment using an AWS EC2 instance running Ubuntu. We’ve streamlined the setup process with helper scripts (thanks to Python), making it straightforward to get the application running once a few prerequisites are met.

We deployed the application exclusively on a free-tier EC2 instance, which provided more than enough resources for our use case. If you’re also using an external database service like Amazon RDS, we recommend setting up the EC2 instance first. This allows for proper configuration and seamless communication between the two services.

### Fork

By forking the GitHub Repository, we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository.
You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/tinobragaa/dublin-bikes)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

### Clone

You can clone the repository by following these steps:

1. Go to the [GitHub Repository](https://github.com/tinobragaa/dublin-bikes) 
2. Locate the Code button above the list of files and click it 
3. Select if you prefer to clone using HTTPS, SSH, or GitHub CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash or Terminal
5. Change the current working directory to the one where you want the cloned directory
6. In your IDE Terminal, type the following command to clone my repository:
	- `git clone https://github.com/tinobragaa/dublin-bikes`
7. Press Enter to create your local clone.