# Sage (health data monitoring service)

### Front-end Web Application

Check out the implementation of the front-end web application here:
https://github.com/RamtinPRG/health_data_monitoring_app

### Table of Contents

- [Overview](#overview)
- [Sage IoT Device Features and Specifications](#sage-iot-device-features-and-specifications)
- [Getting Started with the API](#getting-started-with-the-api)
- [Running the Project](#running-the-project)

## Overview

This project is basically designed and built to be a health data monitoring service. It means hospitals will be able to get and send patient data through the Internet. So the other people that has access to the patient's data (Such as doctors, nurses, hospital admins and families) can get the data and do the analysis. On the other hand, patient is also able to communicate with the hospital, doctors, etc through the Internet. You may be wondering how the data is taken from a patient and sent to hospitals, well I've also designed an IoT device that can easily do this with a low price and a bunch of useful features. Check it out [here](#sage-iot-device-features-and-specifications)!\
The idea behind the project is to increase the efficiency of the healthcare system by reducing the time it takes to get and send data, increasing the security of the data and making it more accessible and decreasing the probability of illness outbreaks. Patients can be able to communicate and be treated by doctors and nurses while they are taking rest at their homes as well, especially if the hospital is located in a remote location or it doesn't have enough beds (which is a big problem for hospitals and we experienced it when Covid-19 was spreading).

## Sage IoT Device Features and Specifications

- ### Specifications

  - **Device Name:** Sage Healthcare Device
  - **Device Type:** IoT Device
  - **Microcontroller:** ESP32 by Espressif
  - **GSM/GPRS:** SIM800L by SIMCOM
  - **Heart Data Sensor:** MAX30102 by MAXIM
  - **Body Temperature Sensor:** DS18B20 by Dallas

- ### Features
  - WiFi to be able to connect to the Internet
  - Bluetooth to connect to nearby devices
  - GSM/GPRS to make phone calls and send SMS whenever the patient doesn't feel well
  - Heart Data Sensor to monitor the heart rate, ECG and SpO2
  - Body Temperature Sensor to monitor the body temperature
  - Send alarm notifications to the hospital when the patient's data is not OK

## Getting Started with the API

### Clone the Repository

Clone the repository using the following command:

```
git clone https://github.com/RamtinPRG/health-data-monitoring-api.git
```

### Install the Dependencies

Ensure you have already installed Python version 3.9.6 or higher. Then install the dependencies using the following command:

```
pip install -r requirements.txt
```

These are the dependencies that you install through the above command:

- asgiref (v3.5.0)
- Django (v4.0.3)
- django-cors-headers (v3.11.0)
- djangorestframework (v3.13.1)
- djangorestframework-simplejwt (v5.1.0)
- PyJWT (v2.3.0)
- pytz (v2022.1)
- sqlparse (v0.4.2)
- tzdata (v2022.1)

### Create the Database

First, you need to make migrations via `manage.py` file created by Django. To do this, run the same thing as below:

```
python manage.py makemigrations api
```

> This will create the `migrations` folder in the `api` folder. Notice that you must not miss the `api` in front of `makemigrations` while you running the command.

Then, migrate the changes to database:

```
python manage.py migrate
```

## Running the Project

Now you can easily run the project by:

```
python manage.py runserver
```

Or even run this if you want to access the server from local network:

```
python manage.py runserver 0.0.0.0:8000
```
