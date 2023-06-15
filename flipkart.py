from pymongo import MongoClient
from gridfs import GridFS
from flask import Flask, redirect, render_template, request, send_file, url_for
from io import BytesIO
import re
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['Flipkart']

fs = GridFS(db)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        description = request.form['image_name'] 
        query = {'description': {'$regex': r'\b' + re.escape(description) + r'\w*', '$options': 'i'}}
        products = db.Products.find(query, {'product_name': 1}).limit(20)
        product_names = list(set(product['product_name'] for product in products))

        if len(product_names) > 0:
            return render_template('search.html', product_names=product_names)
        else:
            return render_template('search.html', error_message='No products found!')

    return render_template('search.html')

@app.route('/product/<name>')
def product_details(name):
    product = db.Products.find_one({'product_name': name})
    return render_template('product_details.html', product=product)


@app.route('/display_image/<filename>')
def display_image(filename):
    filename += '.jpg'
    image_file = fs.find_one({'filename': filename})
    image_data = image_file.read()
    return send_file(BytesIO(image_data), mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)