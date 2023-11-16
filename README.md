# Commerce Application

## Overview
The Commerce Application is a Django-based platform that enables users to participate in various commerce activities, such as browsing products, bidding on items, purchasing products, and selling their own items.

## Installation
To run the Commerce Application locally, follow these steps:

1. Clone the repository: `git clone https://github.com/joshuapramirez/commerce.git`
2. Navigate to the project directory: `cd commerce`
3. Install Django: `pip install django`
4. Apply migrations: `python manage.py makemigrations auctions`
5. Apply migrations to create the database schema: `python manage.py migrate`
6. Create a superuser account for administrative purposes: `python manage.py createsuperuser`
7. Configure the necessary environment variables.

## Usage
1. Start the development server: `python manage.py runserver`
2. Open your browser and go to [http://localhost:8000](http://localhost:8000)
3. Explore products, bid on items, buy and sell products.

## Video Link
[Link to the Commerce Application Video](https://youtu.be/lShJUU4gRe4)

## License
This project is licensed under the [MIT License](LICENSE).
