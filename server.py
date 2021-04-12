from flask import Flask, request, render_template
from flask import jsonify
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:GFHsax21310@10.100.2.83:27017")  #ใส่username and passwd IP ของโหนด MongoDB
db = client["Ass1"]  #ชิ่อของDatabase


@app.route("/")
def hello_world():
    return render_template("index.html")


#/////////////////////////////////////////////////////////////////////////////////

@app.route("/index")
def hello_():
    return render_template("index.html")

@app.route("/AdminEdit")
def AdminEdit():
    return render_template("AdminEdit.html")


@app.route("/About")
def About():
    return render_template("About.html")
    
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/Login")
def Login():
    return render_template("Login.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/Register")
def Register():
    return render_template("Register.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
