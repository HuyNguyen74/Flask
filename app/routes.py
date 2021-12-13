from inspect import _empty
from flask import Flask, render_template, url_for, jsonify, abort
from flask.helpers import flash
from flask.scaffold import _matching_loader_thinks_module_is_package
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.urls import url_parse
from app.forms import RegisterForm,BookForm
from app import app
from app.forms import LoginForm
from flask import redirect,request
from app.models import User,Book,Post
from flask_login import login_user,logout_user,login_required
from flask_login import current_user
from sqlalchemy import func
from app import db
from werkzeug.urls import url_parse
import os

@app.route('/')
@app.route('/index')
@login_required
def index():
    users = [
        {'id': 'u01', 'name': 'huy'},
        {'id':'u02', 'name':'Nguyen'},
        {'id':'u03', 'name':'Thai'}
    ]
    return render_template('index.html', title='Homepage', users=users)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')
    form=LoginForm()
    
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password!=form.password.data:
                flash("password wrong")
                return redirect('/login')
        if user is None:
            flash("not exist")
            return redirect('/login')
        flash('Login {}'.format(form.username.data))
        login_user(user)
        next_page=request.args.get('next')
        if next_page is not None:
            flash('Next page{}'.format(next_page))
            if url_parse(next_page).netloc!='':
                flash('netloc: ' + url_parse(next_page).netloc)
                next_page = '/index'
        else:
            next_page = '/index'
        return redirect(next_page)
        
    return render_template('login.html',form=form)
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        #flash('Register {}'.format(form.username.data))
        user=User.query.filter_by(username=form.username.data).first()
        usermaxid=db.session.query(func.max(User.id)).scalar()
        if form.username.data =='' or form.password.data==''or form.confirm.data==''or form.email.data=='':
            flash("not is empty")
            return redirect('/register')
        if form.password.data!=form.confirm.data:
            flash("confirm password wrong")
            return redirect('/register')

        if user is not None:
            flash("username is existed")
            return redirect('/register')
        if(user is None):
            u1 = User(id=usermaxid+1,username=form.username.data, email=form.email.data,password=form.password.data)
            db.session.add(u1)
            db.session.commit()
            flash("register success")
            return redirect('/index')
        return redirect('/index')
    return render_template('register.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')

@app.route('/upload/',methods=['GET','POST'])
@login_required
def upload():
    form=BookForm()
   
    if form.validate_on_submit():
        bk=Book(bookname=form.bookname.data,author=form.author.data,price=int(form.price.data),img=form.img.data)
        upload_file=request.files['file']
        if upload_file.filename!='':
            upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],upload_file.filename))
          #  bk=Book(bookname=form.bookname.data,author=form.author.data,price=int(form.price.data),img=upload_file.filename)
        db.session.add(bk)
        db.session.commit()
    
        return redirect(url_for('Book_list'))
    return render_template('/upload.html',form=form)

# @app.route('/upload/',methods=['GET','POST'])
# def upload_file():
#     upload_file=request.files['file']
#     if upload_file.filename!='':
#         upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],upload_file.filename))
#         flash("Uploads success")
#     return redirect('/index')
# danh sách book
@app.route('/Mybook/',methods=['GET', 'POST'])
@login_required
def Book_list(): 
    appts = (db.session.query(Book).all())
    return render_template('/index.html', appts=appts)

# Chi tiết sách
@app.route('/books/<int:book_id>/')
@login_required
def book_detail(book_id):
    
    appt = db.session.query(Book).get(book_id)
    if appt is None :
        abort(404)
    return render_template('/detail.html', appt=appt)

@app.route('/books/<int:book_id>/edit/', methods=['GET', 'POST'])
@login_required
def book_edit(book_id):
   
    appt = db.session.query(Book).get(book_id)
    form = BookForm()
    if request.method == 'GET':
        form.bookname.data = appt.bookname
        form.author.data = appt.author
        form.price.data = appt.price
        form.img.data = appt.img
    
    if form.validate_on_submit():
        appt.bookname = form.bookname.data
        appt.author = form.author.data
        appt.price =  form.price.data
       
        upload_file=request.files['file']
        if upload_file.filename!='':
            upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],upload_file.filename))
        appt.img =  upload_file.filename
   
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('book_detail', book_id=appt.id))
    return render_template('/edit.html', form=form)

    #delete
@app.route('/books/<int:book_id>/delete/', methods=['GET'])
@login_required
def book_delete(book_id):
  
    appt = db.session.query(Book).get(book_id)
    if appt is None:
        flash('Appointment not found')
        return redirect('/index')
    db.session.delete(appt)
    db.session.commit()
    
    return redirect('/index')

@app.route('/search/',methods=['GET', 'POST'])
@login_required
def book_search(): 
    book_name=request.args.get("search")
    appts = Book.query.filter(Book.bookname.contains(book_name)).all()
    if appts :
        return render_template('/index.html', appts=appts)
    return render_template('/base.html')
