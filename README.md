# Online Store Project

This project is an online store built using Django, allowing vendors to manage products and customers to browse and purchase them. The project includes features such as product categories, shopping cart, user panels, and order management.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Database Structure](#database-structure)
- [License](#license)

## Project Overview

This is an online store that enables vendors to manage products, apply discounts, and view sales reports. Customers can browse through products, add them to their cart, and complete purchases. Users can sign up with either email or phone number, with SMS verification for phone-based accounts.

## Features

- Vendor panel for managing products, discounts, and orders.
- Customer panel for managing orders and addresses.
- Product browsing with filters like best-selling, highest-rated, and newest.
- Shopping cart with real-time updates.
- User registration and authentication (via email and phone).
- Admin panel for managing the overall store.
- Multi-language support (Persian).

## Technologies

- **Backend**: Python/Django
- **Frontend**: HTML, CSS, Bootstrap, jQuery
- **Database**: SQLite (for development), PostgreSQL (for production)
- **Other**: jdatetime for Persian date handling

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pedram-sardari/OnlineShop-FinalProject.git
   cd project_directory```

2. Create a virtual environment:
  ```python -m venv venv
     source venv/bin/activate  # For Windows: venv\Scripts\activate```

3. Install dependencies:
  ```pip install -r requirements.txt```

4. Set up the database:
  - For development, use SQLite (default)
  - For production, configure PostgreSQL using .env file:
    - DATABASE_URL=postgresql://username:password@localhost:5432/OnlineShop-FinalProject

5. Run migrations:
```python manage.py migrate```

6. Create a superuser for the admin panel:
```python manage.py createsuperuser```

7. Run the development server:
```python manage.py runserver```

## Usage

### Vendor Panel
- Vendors can add/edit products, apply discounts, and manage orders.
  - Access via /vendor-login/.

### Customer Panel
- Customers can view their order history and manage addresses.
  - Access via /customer-login/.

### Shopping Cart
- Customers can add items to the cart, view product details, and complete their purchase.
