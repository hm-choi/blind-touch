from flask import Flask
from service import start_clustering
from conf import *

app = Flask(__name__)

@app.route("/blindtouch", methods = ['GET'])
def auth_api():
    start_clustering()
    return CLUSTERING_2


## Set the port (Default is 8090)
if __name__ == "__main__":              
    app.run(host="0.0.0.0", port="8090")
