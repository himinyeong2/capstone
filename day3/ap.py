from flask import Flask
import numpy as np
import fasttext
from PyKomoran import *

app = Flask(__name__)

@app.route("/")
def index():
    return "test"
    
if __name__ =='__main__':
    app.run(host='0.0.0.0')
