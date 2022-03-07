from flask_bcrypt import Bcrypt
from Website import db, login_manager
from datetime import datetime
from flask_login import UserMixin # auto inherrit the classes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=20),unique=True , nullable = False)
    email_add = db.Column(db.String(length=50),nullable = False,unique=True)
    password_hash = db.Column(db.String(length=60),nullable=False)
    budget = db.Column(db.Integer(),nullable = False,default=100000)
    items = db.relationship('Market' , lazy = True)
    sch = db.relationship('Task' , lazy=True)

    @property
    def display_budget(self):
        self.budget = str(self.budget)
        if len(self.budget)>3:
            return f"{self.budget[:-3]},{self.budget[-3:]}"
        else:
            return self.budget

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = Bcrypt().generate_password_hash(plain_text_password)
    
    def check_password_correction(self,attempted_password):
        return Bcrypt().check_password_hash(self.password_hash , attempted_password)
    
    def can_purchase(self,item_object):
        return self.budget>=item_object.coin_price

    def can_sell(self, item_object):
        return item_object in self.items

class Task(db.Model): 
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(length=50),nullable=False)
    detail = db.Column(db.String(length=200),nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow)
    owner = db.Column(db.Integer() ,db.ForeignKey('user.id'))

    # task1 = Task(title = 'First Task' , detail = "On Terminal")

    def __repr__(self) -> str:
        return f"{self.title}"

class Market(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    coin_id = db.Column(db.Integer , nullable = False)
    coin_slug = db.Column(db.Integer , nullable = False)
    coin_name = db.Column(db.String(length=30),nullable = False,unique=True)
    coin_price = db.Column(db.Integer(),nullable=False)
    coin_total = db.Column(db.Integer(), nullable = False)
    coin_1 =db.Column(db.Integer(), nullable = False)
    coin_24 =db.Column(db.Integer(), nullable = False)
    coin_7 =db.Column(db.Integer(), nullable = False)
    coin_30 =db.Column(db.Integer(), nullable = False)
    coin_info = db.Column(db.String(), nullable = False)
    coin_logo = db.Column(db.String(), nullable = False)
    coin_paper = db.Column(db.String(), nullable = False)
    coin_website = db.Column(db.String(), nullable = False)
    owner = db.Column(db.Integer() , db.ForeignKey('user.id'))

    
    def buy(self,user):
        self.owner = user.id 
        user.budget -= self.coin_price
        db.session.commit()

    def sell(self,user):
        self.owner = None
        user.budget += self.coin_price
        db.session.commit()

    def __repr__(self) -> str:
        return f"{self.coin_name}"
 