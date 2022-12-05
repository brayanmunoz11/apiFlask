from pydoc import apropos
from flask import Flask, jsonify, request
import joblib
import sklearn

app = Flask(__name__)

from products import products

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify({"products": products, "message": "product list"})

@app.route('/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    print(productsFound)
    
    if (len(productsFound)>0):
        return jsonify({"Product": productsFound[0]})
    return jsonify({"message": "Product not found"})


@app.route('/products', methods=['POST'])
def addProducts():
    new_products = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    
    products.append(new_products)
    return jsonify({"message": "products addd successfully", "products": products})

@app.route('/products/<string:product_name>', methods=['PUT'])

def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound)>0):
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({"message": "product Updated","product": productsFound[0]})
    return jsonify({"message": "Product not found"})


@app.route('/products/<string:product_name>', methods=['Delete'])

def deleteProducts(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound)>0):
        products.remove(productsFound[0])
        return jsonify({
            "message": "Product delete",
            "products": products
        })


@app.route('/predict', methods=['POST'])
def addPredict():
    json = request.get_json(force=True)
    edad = json['edad']
    edad_gestacional = json['edad_gestacional']
    peso = json['peso']
    talla = json['talla']
    distrito = json['distrito']
    hemoglobina = json['hemoglobina']
    hbc = json['hbc']
    imc = json['imc']

    medidas = [[edad, edad_gestacional, peso,talla,distrito,hemoglobina,hbc,imc]]

    print(medidas)

    clf =   joblib.load('modelo.pkl')

    pred = clf.predict(medidas)
    pred = int (pred)

    msg = ""

    
    if pred == 0:
        msg = "No tiene anemia"
    if pred == 1:
        msg = "Tiene anemia"
    
   
    body=pred

    
    
    return jsonify({"message": msg , "body": body})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    
