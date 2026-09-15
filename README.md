# 🍽️ SAVOURÉ — Restaurant Management System

**SAVOURÉ** is a Django-based restaurant management system designed to simplify and organize key restaurant operations through a centralized web application.

The system provides separate functionalities for **customers, managers, waiters, kitchen staff, and riders**, allowing different users to perform tasks according to their roles.

##  Live Project

**Website:** https://savoure.com.ng/

**Railway URL:** https://savour-restaurant-production.up.railway.app/

---

##  Project Overview

SAVOURÉ was developed to provide a digital solution for managing restaurant activities such as menu management, customer orders, table reservations, staff management, and kitchen operations.

The application uses **role-based access control** to ensure that users can only access the features relevant to their responsibilities.

### Main User Roles

*  **Manager**
*  **Kitchen Staff**
*  **Waiter**
*  **Rider**
*  **Customer**

---

##  Features

###  Customer

Customers can:

* Create an account
* Log in and log out
* View the restaurant menu
* Browse menu categories
* View food details and prices
* Place food orders
* Choose between dine-in and takeaway orders
* Make table reservations
* View their bookings
* Track their orders
* Manage their customer information

###  Manager

Managers can:

* Access a dedicated manager dashboard
* Create staff accounts
* Assign staff roles
* Register staff phone numbers and addresses
* Create Kitchen Staff and Rider profiles
* Send staff activation emails
* Monitor restaurant operations
* Manage menu categories and menu items
* View restaurant orders
* Monitor table bookings
* Manage restaurant information

###  Kitchen Staff

Kitchen staff have a dedicated dashboard where they can:

* View incoming orders
* See ordered food items
* Monitor orders requiring preparation
* Update food preparation status
* Mark orders as ready

###  Waiter

Waiters can:

* Access a dedicated waiter dashboard
* View relevant customer orders
* Monitor order progress
* Update order/service status
* Assist with dine-in orders

###  Rider

Riders have a dedicated dashboard for managing delivery-related activities.

The system supports:

* Rider profiles
* Vehicle information
* Delivery order management
* Delivery status updates

---

##  Authentication & Authorization

SAVOURÉ uses Django's built-in authentication system together with Django Groups for role-based access control.

Users are assigned to groups such as:

```text
Manager
Waiter
Kitchen Staff
Rider
Customer
```

The application checks the user's role before allowing access to restricted pages.

### Staff Account Activation

Staff accounts are created by a manager and are initially inactive.

The system:

1. Creates the staff account.
2. Generates a secure activation token.
3. Sets an expiration time for the token.
4. Sends an activation email.
5. Allows the staff member to create their own password.
6. Activates the account after successful activation.
7. Removes the activation token after use.

This prevents newly created staff accounts from being used before activation.

---

##  Menu Management

The menu system is organized into categories and menu items.

Example categories include:

* Main Meals
* Starters
* Drinks
* Desserts

Each menu item can contain information such as:

* Name
* Description
* Price
* Category
* Food image
* Availability

---

## 🪑 Table Booking

Customers can reserve restaurant tables by providing information such as:

* Table
* Booking date
* Booking time
* Number of guests
* Booking status

The system supports booking statuses such as:

```text
Pending
Confirmed
Cancelled
Completed
```

Customers can view their bookings from their dashboard.

---

##  Order Management

Customers can place orders using available menu items.

Orders support different order types, including:

```text
Dine-in
Takeaway
```

The order system tracks important information such as:

* Customer
* Ordered items
* Quantity
* Total amount
* Order type
* Order status
* Date and time

Orders can move through different stages as restaurant staff process them.

---

##  Restaurant Order Workflow

A typical order flow is:

```text
Customer
   ↓
Places Order
   ↓
Order Created
   ↓
Kitchen Staff
   ↓
Food Preparation
   ↓
Order Ready
   ↓
Waiter / Rider
   ↓
Customer
   ↓
Order Completed
```

For dine-in orders, the customer's table booking can also be associated with the order.

---

##  Email Integration

The application uses **Resend** for transactional email.

Email functionality is currently used for staff account activation.

The system generates a unique activation link and sends it to the staff member's registered email address.

---

##  Technologies Used

### Backend

* Python
* Django
* Django Authentication
* Django ORM

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite for local development
* Production database configured for deployment

### Email

* Resend

### Deployment

* Railway
* Gunicorn
* WhiteNoise

---

##  Project Structure

```text
RESTAURANT_MANAGEMENT_SYSTEM/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── menu/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── orders/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── tables/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── restaurant_management/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
├── media/
├── manage.py
└── requirements.txt
```

---

##  Running the Project Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Enter the project directory

```bash
cd RESTAURANT_MANAGEMENT_SYSTEM
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

##  Environment Variables

Sensitive information should be stored in environment variables rather than directly in the source code.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=False
RESEND_API_KEY=your-resend-api-key
```

Never commit `.env` files or API keys to GitHub.

---

##  Security

The project uses several Django security features, including:

* Password hashing
* CSRF protection
* Django authentication
* Role-based authorization
* Login-required views
* Secure staff activation tokens
* Environment variables for sensitive configuration
* Inactive accounts before staff activation

---

## 📱 Responsive Interface

The application interface is designed to work across different screen sizes, allowing users to access the system from desktop and mobile devices.

---

## Project Objectives

The main objectives of SAVOURÉ are to:

* Reduce manual restaurant processes
* Improve order management
* Simplify table reservations
* Improve communication between customers and restaurant staff
* Provide role-specific interfaces
* Improve kitchen order tracking
* Centralize restaurant information
* Provide a scalable foundation for future restaurant features

---

##  Future Improvements

Possible future improvements include:

* Online payment integration
* Real-time order notifications
* Advanced sales reports
* Revenue analytics
* Inventory management
* Customer reviews and ratings
* SMS notifications
* More advanced delivery tracking
* Automated order notifications
* Improved manager reporting and analytics

---




© 2026 SAVOURÉ Restaurant Management System
