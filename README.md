# 🌦️ WeatherAppAdvance

A web-based weather forecast application(CRUD Operation) built with **Python (Flask)** and the **OpenWeatherMap API**. Users can input any landmark, city, country, date range and email address to store data and perform CRUD operations. and the app intelligently matches it using fuzzy search to validate date range and get lat & long coordinates.

---

## 🚀 Features

- 📅 **CRUD operation abd Date range weather forecast**  with temperature, description, and icons
- 🌍 Supports global cities and partial/misspelled inputs
- 🧠 Built with Flask and Bootstrap for a clean UI

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, Bootstrap
- **API**: OpenWeatherMap (Forecast)

---

## 📦 Installation

### 1. Clone the repository

git clone https://github.com/dineshkumarmandal/WeatherAppAdvance.git
cd WeatherAppAdvance

### 2. Create Database (MySQL)
    Database Name : weatherappadvance
    Table : 
    CREATE TABLE IF NOT EXISTS `location_details` (
        `ID` int NOT NULL AUTO_INCREMENT,
        `LATITUDE` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
        `LONGITUDE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
        `LANDMARKS` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
        `CITY` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
        `COUNTRY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
        `ZIP_CODE` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
        `FORECAST_START_DATE` date DEFAULT NULL,
        `FORECAST_END_DATE` date DEFAULT NULL,
        `ENTRY_DATE` datetime DEFAULT NULL,
        `FORECAST_DATA` text COLLATE utf8mb4_general_ci,
        `EMAIL_ID` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

### 3. Run the application

```bash
python app.py

Then, Visit http://127.0.0.1:5000 in your browser to access the application.

