
# Store-Manager-api
[![Build Status](https://travis-ci.org/eduhmik/Store-Manager-api.svg?branch=ft-auth-jwt-api-161342719)](https://travis-ci.org/eduhmik/Store-Manager-api)
[![Coverage Status](https://coveralls.io/repos/github/eduhmik/Store-Manager-api/badge.svg?branch=ft-auth-jwt-api-161342719)](https://coveralls.io/github/eduhmik/Store-Manager-api?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/883774545d4244c292db2f22d18eac1e)](https://www.codacy.com/app/eduhmik/Store-Manager-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eduhmik/Store-Manager-api&amp;utm_campaign=Badge_Grade)


Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store. This is an api to help interact with the application in other platforms.

# Required Features
* Store attendant can search and add products to buyer’s cart.
* Store attendant can see his/her sale records but can’t modify them.
* App should show available products, quantity and price.
* Store owner can see sales and can filter by attendants.
* Store owner can add, modify and delete products.

# Optional Features
* Store owner can give admin rights to a store attendant.
* Products should have categories.
* Store attendants should be able to add products to specific categories.

# Technologies
* HTML
* CSS
* Pivotal Tracker
* Python

# Getting Started
* Create a virtual env in your project folder
* git clone https://github.com/eduhmik/Store-Manager.git
* Activate virtual environment
* Install dependencies by running 'pip install -r requirements.txt

# Screenshots
* Coming soon.

# Authors
* **Edwin Kimaita** - *Initial work* - [Eduhmik](https://github.com/Eduhmik)




Endpoint                   | Functionality                |
-------------------------- | -----------------------------
GET /products | Fetch all products           
GET /products/<productId> | Fetch a single product record
GET /sales | Fetch all sale records       
GET /sales/<saleId> | Fetch a single sale record   
POST /products | Create a product             
POST /sales | Create a sale order          
POST /auth/register | Register a user
POST /auth/login | Login a user                 

