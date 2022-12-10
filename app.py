from flask import Flask, jsonify, request
import joblib


app = Flask(__name__)

from products import products

@app.route('/', methods=['GET'])
def getHome():
    return jsonify({"gura": "gura"})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

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
    
