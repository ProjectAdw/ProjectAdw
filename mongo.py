from flask.helpers import url_for
import pymongo
import http.client
import bson
import bcrypt
from flask import Flask,jsonify,render_template,request,redirect,session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

conn = http.client.HTTPSConnection("car-stockpile.p.rapidapi.com")
app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:VIDgnh48123@node12713-project.app.ruk-com.cloud:11012") 
db = client["project"] 


@app.route("/") 
def index(): 
    emp_list = db.car.find().limit(3)
    return render_template('index.html', emp_list = emp_list)

#///////////////////////////////////////////////////////////////////////////

@app.route("/AdminEdit")
def AdminEdit():
    return render_template("AdminEdit.html")

@app.route("/AdminCar")
def AdminCar():
    return render_template("AdminCar.html")

@app.route("/EditCar")
def EditCar():
    return render_template("EditCar.html" )

@app.route("/testupdate")
def testupdate():
    emp_list = db.car.find()
    return render_template("testupdate.html" , emp_list = emp_list)

@app.route("/About")
def About():
    return render_template("About.html")
    
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

########################################################################### LOGIN ###############################################################################################################
@app.route("/Login")
def Login():
    if 'users' in session:
        return 'You are logged in as ' + session['users']
    return render_template("Login.html")

@app.route('/loginBackend', methods=['POST'])
def loginBackend():
    char = db.customer
    login_user = char.find_one({'edd_email' : request.form['email']})
    #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
    if login_user:
        if  bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt()):
            # bcrypt.hashpw(request.form['edd-password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['edd_email'] = request.form['email']
            return redirect(url_for('register'))

    return 'Invalid name/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    char = db.users
    if request.method == 'POST':
        users = char.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'pass' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('Register.html')

###############################################################################################################################################################################################

@app.route("/product")
def product():
    return render_template("product.html")

# @app.route("/Register")
# def Register():
#     return render_template("Register.html")

@app.route("/shop")
def shop():
    shop_list = db.car.find()
    return render_template('shop.html', shop_list = shop_list)

@app.route("/product/<id>")
def clickpro(id):
    pro = db.msg.find_one({'_id': ObjectId(id)})
    return render_template('product.html', pro = pro)


#////////////////////////////////////////////////////////
#ทำการ insert ข้อมูลตารางเข้าไปใหม่
@app.route('/insertuser', methods=['POST'])
def insertuser():
  char = db.customer
  email = request.form['email'] 
  firstname = request.form['firstname']
  lastname = request.form['lastname']
  password = request.form['password']
  coin = request.form['coin']
  address = request.form['address']
  char.insert_one({ 'email' : email, 'firstname' : firstname, 'lastname': lastname, 'password' : password, 'coin':coin , 'address': address})
  return render_template('AdminEdit.html')

@app.route('/insertcar', methods=['POST'])
def insertcar():
  char = db.car
  _name = request.form['_name'] 
  _model = request.form['_model']
  _price = request.form['_price']

  char.insert_one({ '_name' : _name, '_model' : _model, '_price': _price})
  return render_template('AdminCar.html')

#ทำการ edit ข้อมูลตารางโดยการอิง name or _name
@app.route('/update')
def update():
    char = db.car
    id = request.values.get("_id")
    emp_list = char.find({"_id":ObjectId(id)})
    return render_template('EditCar.html',emp_list = emp_list)

@app.route("/action3", methods=['POST'])
def action3 ():
	char = db.Car
	_name=request.values.get("_name")
	_model=request.values.get("_model")
	_price=request.values.get("_price")
	id=request.values.get("_id")
	couteeee = char.update({"_id":ObjectId(id)}, {'$set':{ "_name":_name, "_model":_model, "_price":_price}})

	print(_name)
    
#ทำการ Deleted ข้อมูลตารางโดยการอิง name or _name
@app.route('/deletecar')
def deletecar():
    char = db.Car
    key = request.values.get("_name")
    char.remove({"_name": key})
    return redirect("/testupdate")
#////////////////////////////////////////////////////////

if __name__ == "__main__":
    app.run(host='127.0.0.1',port = 80)