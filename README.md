# 🍔 FoodMart – Online groceries Delivery & E-Commerce Platform

## Overview

FoodMart is a full-stack food delivery and e-commerce web application that enables users to browse food products, add items to their cart, make secure online payments, and track orders seamlessly. The platform is designed to provide a smooth and user-friendly food ordering experience.

## Features

### User Features

* User Registration and Login Authentication
* Browse Food Products by Categories
* Product Search and Filtering
* Add to Cart and Update Quantity
* Secure Checkout Process
* Online Payments using Razorpay
* Order Placement 
* User Profile Management
* Responsive Design for Desktop 

### Admin Features

* Manage Food Products
* Add, Update, and Delete Products
* Manage Customer Orders
* View User Information
* Monitor Order Status

## Payment Integration

FoodMart integrates the Razorpay Payment Gateway to provide secure and reliable online transactions. Users can complete payments directly through the platform, and orders are processed after successful payment verification.

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Django
* Django REST Framework

### Database

* SQLite / MySQL

### Payment Gateway

* Razorpay

### Version Control

* Git & GitHub

## Project Architecture

```text
FoodMart
│
├── Frontend
│   ├── HTML
│   ├── CSS
│   └── JavaScript
│
├── Backend
│   ├── Django
│   ├── REST APIs
│   └── Authentication
│
├── Database
│   └── SQLite/MySQL
│
└── Razorpay Payment Integration
```

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/foodmart-ecommerce.git
```

### 2. Navigate to Project Directory

```bash
cd foodmart-ecommerce
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

### 9. Open Browser

```text
http://127.0.0.1:8000/
```

## API Features

* Product APIs
* User Authentication APIs
* Cart Management APIs
* Order Management APIs
* Payment Processing APIs
* User Profile APIs

## Key Highlights

* Built a complete food ordering platform from scratch.
* Implemented secure authentication and authorization.
* Integrated Razorpay Payment Gateway for online transactions.
* Developed RESTful APIs using Django REST Framework.
* Designed responsive user interfaces for better user experience.
* Implemented cart management and order tracking functionality.

## Future Enhancements

* Live Order Tracking
* Email Notifications
* Product Reviews and Ratings
* Wishlist Functionality
* AI-Based Food Recommendations
* Coupon and Discount System
* Multi-Vendor Support


## Author

**Siddhi Sharma**

Aspiring Full Stack Developer passionate about building scalable web applications using Django, REST APIs, and modern web technologies.

## License

This project is developed for educational and portfolio purposes.
