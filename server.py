from flask import Flask, request, render_template
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


# @app.route("/api/my_json", methods=["GET", "POST"])
# def my_json():
#     if request.method == "POST":
#         data = {"text": "Hello, AdaBrain", "user": "It's me Ada"}

#         return jsonify(data)
#     return "200"


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
