from flask import Flask
from flask_cors import CORS
# from flask_swagger_ui import get_swaggerui_blueprint
import pymongo
from pymongo import MongoClient
from flask import jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

app = Flask(__name__)

# Supporting Cross Origin requests for all APIs
cors = CORS(app)

conf = {
    "mongo_url" : "mongodb+srv://lokv007:lokesh99@mongodb-2fhcm.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE",
    #"host_url": "http://lmp.nupursjsu.net"
    "host": "0.0.0.0"
}

@app.route('/v1/books/<string:Book_id>/recommendations', methods=['GET'])
def get_recommended_books(Book_id):
    response = recommend_books(Book_id)
    return response, 200

def recommend_books(book_id):

	conn=MongoClient(conf['mongo_url'])
	db=conn.Books
	coll=db.library_books_new

	books = pd.read_csv('userRatings.csv')

	#create a pivot table
	books_pivot = books.pivot(index='bookTitle',columns = 'userID', values = 'bookRating').fillna(0)
	books_matrix = csr_matrix(books_pivot.values)
	model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
	model_knn.fit(books_matrix)

	query_index = int(book_id)
	distances, indices = model_knn.kneighbors(books_pivot.iloc[query_index,:].values.reshape(1,-1),n_neighbors=6)
	l = []
	for i in range(0,len(distances.flatten())):
		if i != 0:
			l.append(indices.flatten()[i])

	output = []
	for j in l:
		get = coll.find({'bookID' : str(j)}, {'_id' : False})
		for i in get:
			output.append(i)
	return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
    # app.run(host=conf['host'], port=conf['port'], debug=True)
