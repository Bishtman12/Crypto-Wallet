from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from Website.Models import User

class RegisterForm(FlaskForm): # auto checks all validate functions

    def validate_username(self,username_to_check): #checks if there is a field with 
        #name of username if exist then the fucntion is executed
        user = User.query.filter_by(username = username_to_check.data).first()
        if user: 
            raise ValidationError('Username Already Exist')
    
    def validate_email_add(self,email_check):
        email = User.query.filter_by(email_add = email_check.data).first()
        if email: 
            raise ValidationError('Account Already Exist with this Email.')

    username = StringField(label='Username' ,validators=[Length(min=4,max=20),DataRequired()])
    email_add = StringField(label='Email Address',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password',validators=[Length(min=6,max=20),DataRequired()])
    password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create New Account')

class TaskForm(FlaskForm):
    title = StringField(label='Title' ,validators=[DataRequired()])
    detail = StringField(label='Details',validators=[DataRequired()])
    submit = SubmitField(label='Create Task')

class LoginForm(FlaskForm):
    username = StringField(label='Username' ,validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Log In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Confirm Buy')

class UpdateForm(FlaskForm):
    title = StringField(label='Title' ,validators=[DataRequired()])
    detail = StringField(label='Details',validators=[DataRequired()])
    submit = SubmitField(label='Update Task')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Confirm Sell')


 