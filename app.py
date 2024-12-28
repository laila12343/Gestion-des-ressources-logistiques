from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf.csrf import CSRFProtect
import os
import json
import random
import pandas as pd
app = Flask(__name__)
app.secret_key = 'sakhta-secret-key'
csrf = CSRFProtect(app)
# Mock Databases
users = {"user1": {"name": "John", "email": "john@example.com", "password": "1234"}}
orders = {"user1": [{"id": 1, "status": "Delivered"}, {"id": 2, "status": "In preparation"}]}
feedbacks = []
# File paths
data_file = "shop_items.json"
excel_file = "DataBase.xlsx"

# Check if the data file exists
if os.path.exists(data_file):
    # Load the dictionary from the JSON file
    with open(data_file, "r") as file:
        shop_items = json.load(file)
else:
    # Read the Excel file
    shop_items = {}
    df = pd.read_excel(excel_file)

    # Iterate through the rows of the Excel file
    for _, row in df.iterrows():
        item_id = row['ID']  # Random 4-digit ID
        prod_name = row['Short_Name']  # Replace with the actual column name
        prod_detail = row['Details']  # Replace with the actual column name
        prod_price = round(row['actual_price'], 2)  # Replace with the actual column name
        prod_stock = random.randint(0, 50)  # Replace with the actual column name
        prod_available = prod_stock > 0  # Determine availability
        link=row['Image'].replace("https://m.media-amazon.com/images/I/", "")
        img_url = f"img/{link}"  # Replace with the actual column name

        # Add the item to the dictionary
        shop_items[item_id] = {
            "name": prod_name,
            "detail": prod_detail,
            "price": prod_price,
            "stock": prod_stock,
            "is_available": prod_available,
            "img": img_url,
        }

    # Save the dictionary to a JSON file
    with open(data_file, "w") as file:
        json.dump(shop_items, file)

# Generate a cart dictionary based on desired product names
desired_names = ["GUESS Gradient Butterfly", "boAt Airdopes 141", "Oppo Enco M32"]

cart = {
    key: {**value, "quantity": random.randint(1, 4)}
    for key, value in shop_items.items()
    if value["name"] in desired_names
}

@app.context_processor
def inject_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return dict(csrf_token=generate_csrf())
#shop_items = {item for filename in os.listdir(img_folder) if filename.endswith((".png", ".jpg", ".jpeg"))]
#print(sum(item['price'] * item['quantity'] for item in cart.values()))
# ---------------- User Authentication ----------------

@app.route('/account')
def account():
    customer = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com'
    }
    addresses = [
        {'home_address': '123 Main St', 'bus_stop': 'Central', 'city': 'Springfield', 'state': 'IL'}
    ]
    myaddress = True
    return render_template('myaccount.html', customer=customer, addresses=addresses, myaddress=myaddress)


@app.route('/')
def index():
    #num_of_items = len(cart)
    return render_template('index.html', user_authenticated=True, user_name="John", cart=cart)

@app.route('/shop')
def show_gallery():
    #img_folder = os.path.join(app.static_folder, "img")
    images = [shop_items[item]['img'] for item in shop_items]
    return render_template('gallery.html',images=images, shop_items=shop_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        for username, details in users.items():
            if user == details['email'] and details['password'] == request.form['password']:
                session['user'] = username
                return redirect(url_for('profile'))
        return "Login Failed"
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ---------------- Personal Space Page ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    if request.method == 'POST':
        users[user]['name'] = request.form['name']
        users[user]['email'] = request.form['email']
        return "Profile Updated Successfully!"
    return render_template('profile.html', user=users[user])


# ---------------- Shopping Cart ----------------
@app.route('/cart')
def shop_cart():
    #cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

def update_cart_item(product_id, quantity):
    #cart = session.get('cart', {})
    if product_id in [element['id'] for element in cart.values()]:
        cart[product_id]['quantity'] = quantity
        session['cart'] = cart
    pass    



@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    #session.setdefault('cart', {})
    #cart={"num_of_items": 5}
    #cart = session['cart']
    #product_id = str(product_id)
    if product_id in shop_items:
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            prod_by_id=shop_items[product_id]
            cart[product_id] = {'name':prod_by_id['name'],'price':prod_by_id['price'] ,'quantity': 1,'img': prod_by_id['img']}
        session['cart'] = cart
        session.modified = True
    else:
        return "Product not found"
    # Redirect back to the page the user was on
    return render_template('gallery.html', shop_items=shop_items)
    #return redirect(url_for('cart'))



@app.route('/delete_from_cart/<int:product_id>')
def delete_from_cart(product_id):
    cart = session.get('cart', {})
    #cart={"num_of_items": 5}
    cart.pop(product_id, None)
    session['cart'] = cart
    return redirect(url_for('cart'))


# ---------------- Shopping Summary Page ----------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ShippingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/checkout')
def checkout():
    token = session.get("_csrf_token")
    #cart = session.get('cart', {})
    #cart={"num_of_items": 5}
    # = request.user.customer
    #cartitems = list(cart.values())
    #form = ShippingForm()
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    context = {'cart': cart #,'form':form
               #'cartitems':cartitems, #'customer_address': customer_address
               }
    return render_template('checkout.html', cart=cart, total=total,csrf_token=token,context=context)


# ---------------- Order Tracking ----------------
@app.route('/order_status')
def order_status():
    user_orders = orders.get(session.get('user', ''), [])
    return render_template('order_status.html', orders=user_orders)


@app.route('/update_order_status/<int:order_id>/<status>')
def update_order_status(order_id, status):
    for order in orders.get(session.get('user', ''), []):
        if order['id'] == order_id:
            order['status'] = status
    return jsonify({"message": "Order status updated!"})


# ---------------- Feedback Page ----------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        fb = {"user": session.get('user', 'Anonymous'), "message": request.form['message']}
        feedbacks.append(fb)
        return "Feedback submitted!"
    return render_template('feedback.html')


# ---------------- Chat Box ----------------
@app.route('/chat')
def chat():
    return render_template('chat.html')


# ---------------- Notifications ----------------
@app.route('/notifications')
def notifications():
    # Mock notifications for order updates
    user_notifications = [
        {"message": "Your order #1 has been delivered."},
        {"message": "Your order #2 is in preparation."}
    ]
    return render_template('notifications.html', notifications=user_notifications)


# ---------------- Run the App ----------------
if __name__ == '__main__':
    app.run(debug=True)
