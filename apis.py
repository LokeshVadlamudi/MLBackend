from functions import *
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import json
import pymongo

app = Flask(__name__)

# Supporting Cross Origin requests for all APIs
cors = CORS(app)

conf = {
    "mongo_url" : "mongodb+srv://lokv007:lokesh99@mongodb-2fhcm.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE",
    #"host_url": "http://lmp.nupursjsu.net"
    "host": "http://localhost"
}

@app.route('/v1/books/<string:Book_id>/recommendations', methods=['GET'])
def get_recommended_books(Book_id):
    response = recommend_books(Book_id)
    return response, 200


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080)
    # app.run(host=conf['host'], port=conf['port'], debug=True)