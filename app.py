from flask import Flask, jsonify, request, render_template
import joblib
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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

@app.route('/predictv2', methods=['POST'])
def addPredictv2():
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

    clf1 =   joblib.load('modeloNBayes98perc.pkl')

    pred = clf1.predict(medidas)
    print(pred)
    return jsonify({"message": str(pred[0]), "Status": 200})

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=4000)
    
