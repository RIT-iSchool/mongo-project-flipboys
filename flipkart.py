from bson import ObjectId
from pymongo import MongoClient
from gridfs import GridFS
from flask import Flask, redirect, render_template, request, send_file, url_for
from io import BytesIO
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['Flipkart']

fs = GridFS(db)

# Main starting page of the web application.
@app.route('/')
def main_page():
    return render_template('index.html')

# Search based on description or geospatial input.
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_option = request.form.get('search_option')
        if search_option == 'description':
            description = request.form.get('description')
            if not description:
                return render_template('search.html', error_message='Description not specified for product search', search_option=search_option)
            query = {'description': {'$regex': r'\b' + re.escape(description) + r'\w*', '$options': 'i'}}
            products = db.Products.find(query, {'product_name': 1}).limit(20)
            product_names = list(set(product['product_name'] for product in products))

            if len(product_names) > 0:
                return render_template('search.html', product_names=product_names, search_option=search_option)
            else:
                return render_template('search.html', error_message='No products found!', search_option=search_option)
        
        elif search_option == 'geospatial':
            longitude = request.form.get('longitude')
            latitude = request.form.get('latitude')
            if not longitude or not latitude:
                return render_template('search.html', error_message='No Geospatial data', search_option=search_option)
            longitude = float(longitude)
            latitude = float(latitude)

            query = {'location': {'$near': {'$geometry': {'type': 'Point', 'coordinates': [longitude, latitude]}, '$maxDistance': 100000}}}
            products = db.Products.find(query, {'product_name': 1}).limit(20)
            product_names = list(set(product['product_name'] for product in products))

            if len(product_names) > 0:
                return render_template('search.html', product_names=product_names, search_option=search_option)
            else:
                return render_template('search.html', error_message='No products found!', search_option=search_option)

    return render_template('search.html')

# Display product details once the user selects the product.
@app.route('/product/<name>')
def product_details(name):
    product = db.Products.find_one({'product_name': name})
    return render_template('product_details.html', product=product)

# Display the image associated with the product.
# If image not found, display default flipkart image.
@app.route('/display_image/<filename>')
def display_image(filename):
    filename = './images/' + filename + '.jpg'
    image_file = fs.find_one({'filename': filename})
    image_data = image_file.read()
    return send_file(BytesIO(image_data), mimetype='image/jpg')

# Get comments from the user and update the database.
@app.route('/add_comment', methods=['POST'])
def add_comment():
    product_id = request.form['product_id']
    comment = request.form['comment']

    db.Products.update_one(
        {'_id': ObjectId(product_id)},
        {'$push': {'comment': comment}}
    )

    name = request.form['name']

    return redirect(url_for('product_details', name=name))

# Run the flask server
if __name__ == '__main__':
    app.run(debug=True)