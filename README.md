[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11318438&assignment_repo_type=AssignmentRepo)

Database Source and Description:

We have used the Flipkart Product database from Kaggle. Flipkart is an Indian E-commerce company headquatered in Bengaluru, India.
Source - https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products

The above dataset consists of 20000 products. We did the following operations on the database to get it ready for MongoDB project - 
1. Trim the database to have only 3000 products. (We selected first 3000 products)
2. Add latitude and longitude values of the store locations in India. (To run the geospatial queries)
3. The dataset had links to images, not the actual images. Hence, we wrote a python script to fetch and download those images. 
4. We numbered the images from 0 to 2999, with each image co-relating to every product. Further we added "product_number" to the CSV file where
   the products are numbered from 0 to 2999. This allows co-relation between products and the associated images.
5. We also added a default images to display for products whose images are missing.


Technology Stack:

1. MongoDB for Backend
2. HTML, CSS, JavaScript
3. Python (Flask Framework) - Rendered HTML templates with flask using Jinja.

Steps to run application:

1. Run flipkart.py to start the server for web application.
2. Open a browser to visit http://localhost:5000/ (This is the default Flask server)

Tech Stack Justification and Use:

Flask with HTML made frontend easier, this allowed us to focus on MongoDB queries for backend to complete the given tasks.

Folder Structure - 

1. flipkart.py - Web app server for searching flipkart products.
2. templates -
   - index.html
   - search.html
   - product_details.html
3. UpdateLocationField.js - update location using latitude and longitude (lecture code)

To Create index - db.Products.createIndex({location: '2dsphere'})
Field to store user comments - db.Products.updateMany({}, { $set: { comment: [] } }) 

Note  - 

1. We have kept the search limit to be 20. This can be increased if needed in flipkart.py
