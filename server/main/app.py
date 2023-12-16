from flask import Flask,send_file,request
from service import start_clustering
import time

app = Flask(__name__)
SHARE_PATH = 'Path of the stored ciphertext from the main server \
             (The client\'s encrypted feature vector is given to the Main server, then the main server stored it in this path.)'

@app.route("/blindtouch", methods = ['POST'])
def auth_api():
    f = request.files['target_enc']
    f.save(SHARE_PATH)
    START_TIME = time.time()
    RESULT_PATH = start_clustering()
    return send_file(RESULT_PATH,as_attachment=True)

## Set the port (Default is 8090)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8090")
