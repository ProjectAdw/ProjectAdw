from flask.helpers import url_for
import pymongo
import http.client
import bcrypt
from flask import Flask,jsonify,render_template,request,redirect,session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from bson import json_util

conn = http.client.HTTPSConnection("car-stockpile.p.rapidapi.com")
app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:VIDgnh48123@node12713-project.app.ruk-com.cloud:11012") 
db = client["project"] 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/") 
def index(): 
    emp_list = db.car.find().limit(3)
    if 'email' in session:
        ses = 'You are logged in as ' + session['email']

    return render_template('index.html', emp_list = emp_list , ses = ses)

#///////////////////////////////////////////////////////////////////////////

@app.route("/Car", methods=['GET','POST','PUT'])
def get_allCar():
    char = db.car #เป็นเหมือนการนำค่าชื่อหัวตารางมาใส่ในตัวแปร char
    output = []
    for x in char.find(): #ทำตามฟังชั่น
        output.append({'_id' : x['_id'],'_name' : x['_name'],'_model' : x['_model'],
                        '_price' : x['_price']}) #เอาค่าในตารางมาอ่านแล้วใส่ไปใน output เป็นเหมือนค่าอาเร
    return json_util.dumps(output) #หลังจากทำเงื่อนไขเสร็จส่งค่ากลับไปที่ output

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
@app.route("/login")
def login():
    if 'email' in session:
        return 'You are logged in as ' + session['email']

    return render_template('Login.html')

@app.route('/loginBackend', methods=['POST'])
def loginBackend():
    users = db.customer
    email = request.form.get("email")
    password = request.form.get("password")
    login_user = users.find_one({'email': request.form['email']})

    if login_user:
        email_val = login_user['email']
        passwordcheck = login_user['password']

        if bcrypt.checkpw(password.encode('utf-8'),passwordcheck):
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return 'Invalid email or password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    char = db.customer
    if request.method == 'POST':
        users = char
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = request.form['password']
            emaila = request.form['email']
            users.insert_one({'username' : request.form['username'], 'password' : hashpass , 'email':emaila})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return render_template('index.html')

    return render_template('Register.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
###############################################################################################################################################################################################

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/Register")
def Register():
    return render_template("Register.html")

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
    char = db.car
    _name=request.values.get("_name")    
    _model=request.values.get("_model")    
    _price=request.values.get("_price")       
    id=request.values.get("_id")    
    char.update_one({"_id":ObjectId(id)}, {'$set':{ "_name": _name, "_model":_model, "_price":_price}})    
    return redirect("/shop")    
	
    
#ทำการ Deleted ข้อมูลตารางโดยการอิง name or _name
@app.route('/deletecar')
def deletecar():
    char = db.car
    key = request.values.get("_name")
    char.remove({"_name": key})
    return redirect("/testupdate")

@app.route("/get_user", methods=["GET", "POST"])
def get_user():
    output = []
    for post in db.find():
        output.append(
            {post["_id"], post["_name"], post["_model"], post["_price"]}
        )
    return json_util.dumps(output)
#////////////////////////////////////////////////////////

if __name__ == "__main__":
    app.run(host='127.0.0.1',port = 80)