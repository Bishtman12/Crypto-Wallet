from datetime import datetime
from Website import app
from flask import flash, redirect, render_template, url_for,get_flashed_messages,request
from Website.Models import Market, Task, User
from Website.forms import LoginForm, PurchaseItemForm, RegisterForm, SellItemForm, TaskForm, UpdateForm
from Website import db
from flask_login import login_user, logout_user, login_required, current_user
from Website.update_coins import update_coin

@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home.html')

@app.route('/task/', methods=['GET','POST'])
@login_required
def schedule():
    form = TaskForm()
    print("Comes")
    if form.validate_on_submit():
        print("Done")
        task_to_create = Task(title = form.title.data , detail= form.detail.data,
        owner=current_user.id)
        print("Done")
        db.session.add(task_to_create)
        db.session.commit()    
        return redirect(url_for('schedule'))    
        # except IntegrityError:
        #     db.session.rollback()
    print("Done outside submit")
    tasks = Task.query.filter_by(owner=current_user.id)
    return render_template('tasks.html',tasks = tasks , form=form)


@app.route('/schedule/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('schedule'))


@app.route('/schedule/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    article = Task.query.get(id)
    form = UpdateForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        return redirect(url_for('schedule'))
    return render_template("update.html", form=form)

@app.route('/market/',methods=["POST","GET"])
@login_required
def market():

    #updating the coins data via API
    # update_coin()


    #responsive 
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    # print(purchase_form['submit']) #returns an html code
    if request.method == "POST":
        # Purchase coin logic
        purchased_item = request.form.get('purchased_item')
        print(purchased_item)
        p_item_object = Market.query.filter_by(coin_name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congrats! You just purchased{p_item_object.coin_name}",category='success')
            else:
                flash(f"Sorry! You don't have enough Mney :(" , category='danger')
        # selling coin logic
        sold_item = request.form.get('sold_item')
        s_item_object = Market.query.filter_by(coin_name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congrats! You just sold{s_item_object.coin_name}",category='success')
            else:
                flash(f"Something went Wrong. You don't own any coins")
        return redirect(url_for('market'))

    if request.method == "GET":
        # items = Market.query.filter_by(owner = None) # if want to hide 
        items = Market.query.all()
        owned_items = Market.query.filter_by(owner= current_user.id)
        return render_template('market.html' , items = items , purchase_form=purchase_form,owned_items=owned_items, selling_form=selling_form)

@app.route('/success')
def success():
    return render_template('sucess.html')

@app.route('/logout' , methods=['GET','POST'])
def logout_page():
    logout_user()
    flash ( "You have been logged out", category='info')
    return redirect(url_for('home_page'))

@app.route('/login' , methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_try = User.query.filter_by(username=form.username.data).first()
        if user_try and user_try.check_password_correction(attempted_password=form.password.data):
            
            login_user(user_try)
            flash (f"You're logged in as {user_try.username}", category="success")
            return redirect(url_for('home_page'))
        else:
            flash("Username and password do not match Try Again", category='danger')

    return render_template(('login.html') , form = form)


@app.route('/register' , methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
        email_add=form.email_add.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()        
        # except IntegrityError:
        #     db.session.rollback()
        return redirect(url_for('success'))
    if form.errors != {}:
        for x in form.errors.values():
            flash(f"There was an error with creating a user : {x}" ,  category='danger')
    return render_template('forms.html' , form = form)

