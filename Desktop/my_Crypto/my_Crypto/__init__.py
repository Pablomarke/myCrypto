from flask import Flask
from key import APIKEY

app = Flask(__name__)

from my_Crypto.routes import *