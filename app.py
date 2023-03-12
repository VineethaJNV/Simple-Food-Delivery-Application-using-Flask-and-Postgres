from flask import Flask, render_template,request,flash, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/menu_details'
app.config['SECRET_KEY'] = '8BQ\xc6\xf7\xa8\rq*~h\xf3\xaf\x12z\xde\x15cf\xf6>j\xda\xe5'


db = SQLAlchemy(app)

class Menu(db.Model):
    __tablename__ = 'menu_details'
    menu_id = db.Column(db.Integer, primary_key = True)
    food_items = db.Column(db.String(length = 60), nullable = False)
    # price = db.Column(db.Integer, nullable = False, default = 75)
    # date_added = db.Column(db.DateTime, default = datetime.utcnow)

class Food(db.Model):
    __tablename__='orders'

    order_id = db.Column(db.Integer, primary_key = True, nullable = False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_details.menu_id'))
    description = db.Column(db.String(length = 60), nullable = False)
    # price = db.Column(db.Integer, nullable = False, default = 75)
    # date_ordered = db.Column(db.DateTime, default = datetime.utcnow)
    # def __repr__(self) -> str:
    #     return f"{self.order_id} - {self.description} - {self.price} - {self.date_ordered}"
    menu = db.relationship("Menu")
    

@app.route("/")
def show_menu():
    return render_template("index.html", menu_details = Menu.query.all())

@app.route("/menu/<menu_id>/varieties")
def show_food(menu_id):
    return render_template("menu-tasks.html",  id_num = Menu.query.filter_by(menu_id = menu_id).first(), menu_details = Menu.query.all(), varity = Food.query.filter_by(menu_id = menu_id).first())

@app.route("/add/menu", methods = ['POST'])
def add_order():
    if not request.form['menu-title']:
        flash("Search for your favourite food","red")
        
    else:
        menu = Menu(food_items=request.form['menu-title'])
        db.session.add(menu)
        db.session.commit()
        flash("Your favourite food is added successfully","green")
    return redirect(url_for('show_menu'))

@app.route("/place/order/<menu_id>", methods = ['POST'])
def add_task(menu_id):
    if not request.form['placed-order']:
        flash("Enter the food you want to order","red")
    else:
        order = Food(description = request.form['placed-order'])
        db.session.add(order)
        db.session.commit()
        flash("Thank you for choosing us","green")
        flash("Your order details are as follows","white")
        flash(f"-{order.order_id} - {order.description}","white") #- {Food.price} {Food.date_ordered}")
        flash("Food ordered successfully, Your food will be delivered anytime in next 20 minutes","white")
    return redirect(url_for('show_food', menu_id = menu_id))
app.run(debug=True, host = "127.0.0.1", port = 5000)