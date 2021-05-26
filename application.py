import os
from flask import Flask, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import jwt
import sqlalchemy
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres','postgresql')
import models
models.db.init_app(app)



# Root notification
def root():
    return 'May the force be with you.'
app.route('/', methods=["GET"])(root)


# Seeding kyber crystal inventory
def seed():
    light1s = models.Product(
        name = "Tranquility",
        description = "A vibrant kyber crystal with a green hue, perfect for a force-wielder with a calm and wise disposition.",
        image = "https://i.pinimg.com/originals/8b/1d/b1/8b1db129a61fb67f791dec4a12cddc73.png",
        price = 1299,
        type = "single",
        force = "light"
    )
    light1d = models.Product(
        name = "Tranquility",
        description = "A pair of vibrant kyber crystals with a green hue, perfect for a force-wielder with a calm and wise disposition.",
        image = "https://i.pinimg.com/originals/8b/1d/b1/8b1db129a61fb67f791dec4a12cddc73.png",
        price = 2499,
        type = "double",
        force = "light"
    )
    light2s = models.Product(
        name = "Disicipline",
        description = "A radiant kyber crystal with a purple hue, perfect for a force-wielder disciplined in both the force and combat.",
        image = "https://i.pinimg.com/originals/eb/48/18/eb4818dbb45c0ddfe6d575e72161d22b.png",
        price = 1299,
        type = "single",
        force = "light"
    )
    light2d = models.Product(
        name = "Disicipline",
        description = "A pair of radiant kyber crystals with a purple hue, perfect for a force-wielder disciplined in both the force and combat.",
        image = "https://i.pinimg.com/originals/eb/48/18/eb4818dbb45c0ddfe6d575e72161d22b.png",
        price = 2499,
        type = "double",
        force = "light"
    )
    dark1s = models.Product(
        name = "Power",
        description = "A dominating kyber crystal with a crimson hue, perfect for a force-wielder seeking to overwhelm and overpower any opponents.",
        image = "https://i.pinimg.com/originals/7b/62/c9/7b62c9368c9b701f8182bc8af9cb13df.png",
        price = 1299,
        type = "single",
        force = "dark"
    )
    dark1d = models.Product(
        name = "Power",
        description = "A pair of dominating kyber crystals with a crimson hue, perfect for a force-wielder seeking to overwhelm and overpower any opponents.",
        image = "https://i.pinimg.com/originals/7b/62/c9/7b62c9368c9b701f8182bc8af9cb13df.png",
        price = 2499,
        type = "double",
        force = "dark"
    )
    dark2s = models.Product(
        name = "Corruption",
        description = "A destructive kyber crystal with a blood-red hue, perfect for a force-wielder seeking to corrupt and control all.",
        image = "https://i.pinimg.com/originals/7b/62/c9/7b62c9368c9b701f8182bc8af9cb13df.png",
        price = 1299,
        type = "single",
        force = "dark"
    )
    dark2d = models.Product(
        name = "Corruption",
        description = "A pair of destructive kyber crystals with a blood-red hue, perfect for a force-wielder seeking to corrupt and control all.",
        image = "https://i.pinimg.com/originals/7b/62/c9/7b62c9368c9b701f8182bc8af9cb13df.png",
        price = 2499,
        type = "double",
        force = "dark"
    )          
    models.db.session.add(light1s)
    models.db.session.add(light1d)
    models.db.session.add(light2s)
    models.db.session.add(light2d)
    models.db.session.add(dark1s)
    models.db.session.add(dark1d)
    models.db.session.add(dark2s)
    models.db.session.add(dark2d)
    models.db.session.commit()

    return { "message": "Seed successful" }

app.route('/seed', methods=["GET"])(seed)


# Register new user
def create_user():
    hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode("UTF-8")
    user = models.User(
        name = request.json["name"],
        email = request.json["email"],
        password = hashed_pw
    )
    models.db.session.add(user)
    models.db.session.commit()

    encrypted_id = jwt.encode({ "user_id": user.id }, os.environ.get('JWT_SECRET'), algorithm="HS256")

    return {
        "message": "User created successfully",
        "user": user.user_info_payload(),
        "user_id": encrypted_id
    }
app.route('/users/register', methods=["POST"])(create_user)


# Login existing user
def login_user():
    user = models.User.query.filter_by(email = request.json['email']).first()
    if not user:
        return { "message": "User not found" }, 404

    if bcrypt.check_password_hash(user.password, request.json['password']):
        encrypted_id = jwt.encode({ "user_id": user.id }, os.environ.get('JWT_SECRET'), algorithm="HS256")

        return {
            "message": "User login successful",
            "user": user.user_info_payload(),
            "user_id": encrypted_id
        }

    else:
        return { "message": "Password is incorrect" }, 401
app.route('/users/login', methods={"POST"})(login_user)


# Verify existing user
def verify_user():
    decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])["user_id"]
    user = models.User.query.filter_by(id = decrypted_id).first()
    if not user:
        return { "message": "user not found"}, 404

    encrypted_id = jwt.encode({ "user_id": user.id }, os.environ.get('JWT_SECRET'), algorithm="HS256")

    return {
        "message": "User created successfully",
        "user": user.user_info_payload(),
        "user_id": encrypted_id
    }
app.route('/users/verify', methods=["GET"])(verify_user)


# Retrieve products as single, all, force side, and type
def get_one_product(id):
    product = models.Product.query.filter_by( id = id ).first()

    return { "product": product.product_payload() }
app.route('/products/<int:id>', methods=["GET"])(get_one_product)

def get_all_products():
    products = models.Product.query.all()

    return { "products": [p.product_payload() for p in products] }
app.route('/products', methods=["GET"])(get_all_products)

def get_all_light():
    light_side = models.Product.query.filter_by( force = "light" ).all()

    return { "products": [l.product_payload() for l in light_side] }
app.route('/products/light', methods=["GET"])(get_all_light)

def get_all_dark():
    dark_side = models.Product.query.filter_by( force = "dark" ).all()

    return { "products": [d.product_payload() for d in dark_side] }
app.route('/products/dark', methods=["GET"])(get_all_dark)

def get_all_single_type():
    single_type = models.Product.query.filter_by( type = "single" ).all()

    return { "products": [t.product_payload() for t in single_type] }
app.route('/products/single', methods=["GET"])(get_all_single_type)

def get_all_double_type():
    double_type = models.Product.query.filter_by( type = "double" ).all()

    return { "products": [t.product_payload() for t in double_type] }
app.route('/products/double', methods=["GET"])(get_all_double_type)


# Retrieve cart, add item to cart, delete item from cart
def get_cart():
    pass
app.route('/cart', methods=["GET"])(get_cart)

def add_item_cart():
    pass
app.route('/cart/add', methods=["POST"])(add_item_cart)

def remove_item_cart():
    pass
app.route('/cart/remove', methods=["DELETE"])(remove_item_cart)


# Retrieve single order, retrieve all orders, create order
def get_single_order(id):
    pass
app.route('/orders/<int:id>', methods=["GET"])(get_single_order)

def get_all_orders():
    pass
app.route('/orders', methods=["GET"])(get_all_orders)

def create_order():
    pass
app.route('/orders/new', methods=["POST"])(create_order)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)