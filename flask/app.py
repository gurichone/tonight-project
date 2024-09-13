from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
  name = "Good morning m〇ther f〇ckers!!"
  return name
