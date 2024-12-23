from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.secret_key = 'sakhta-secret-key'
csrf = CSRFProtect(app)
# Mock Databases
users = {"user1": {"name": "John", "email": "john@example.com", "password": "1234"}}

products = [
    {"id": 1, "name": "Product A", "price": 100},
    {"id": 2, "name": "Product B", "price": 200},
    {"id": 3, "name": "Product C", "price": 300},
]
orders = {"user1": [{"id": 1, "status": "Delivered"}, {"id": 2, "status": "In preparation"}]}
feedbacks = []
cart = {
    "1": {  # Product ID as the key (string)
        "id": 1,          # Product ID
        "name": "Laptop", # Product name
        "price": 1000.0,  # Price per unit
        "quantity": 2, # Quantity of the product
        "image": "laptop.jpg"
    },
    "2": {  # Another product in the cart
        "id": 2,
        "name": "Mouse",
        "price": 50.0,
        "quantity": 1,
        "image": "mouse.jpg"
    },
    "3": {
        "id": 3,
        "name": "Camera",
        "price": 750.0,
        "quantity": 1,
        "image": "camera.jpg"
    },
}
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
    
    num_of_items = len(cart)
    return render_template('index.html', user_authenticated=True, user_name="John", cart=cart, products=products)

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
    return render_template('cart.html', cart=cart, products=products, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    session.setdefault('cart', {})
    #cart={"num_of_items": 5}
    cart = session['cart']
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'id': product_id, 'quantity': 1}
    session['cart'] = cart
    return redirect(url_for('cart'))


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
    return render_template('checkout.html', cart=cart, products=products, total=total,csrf_token=token,context=context)


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
