from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    is_ordered = db.Column(db.Boolean)

    products = db.relationship("Product", backref="product")

    def cart_payload(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "is_ordered": self.is_ordered,
        }

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    total = db.Column(db.Integer)

    cart = db.relationship("Cart", backref="cart")

    def order_payload(self):
        return {
            "id": self.id,
            "total": self.total
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Integer)
    type = db.Column(db.String)
    force = db.Column(db.String)

    def product_payload(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "price": self.price,
            "type": self.type,
            "force": self.force
        }
    

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.String)
    current = db.Column(db.Integer)
    lifetime = db.Column(db.Integer)

    orders = db.relationship("Order", backref="order")
    cart = db.relationship("Cart")

    def user_info_payload(self):
        return {
            "name": self.name,
            "email": self.email
        }
    
    def user_address_payload(self):
        return {
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode
        }
    
    def user_loyalty_payload(self):
        return {
            "current": self.current,
            "lifetime": self.lifetime
        }

