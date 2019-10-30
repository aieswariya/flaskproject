from newflask import flaskapp, db
from flask import render_template, Flask, flash, redirect ,request,url_for
from newflask.forms import LoginForm, RegistrationForm ,SearchForm ,UpdateForm ,BlogForm 
from flask_login import current_user
from newflask.base import session
from newflask.models import User ,Blog ,OAuthSignIn
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import update


@flaskapp.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@flaskapp.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider( provider)
    username,email = oauth.callback()
    if email is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    
    
    user=session.query(User).filter_by(email='email').first()
    if not user:
        nickname = username
        if nickname is None or nickname == " ":
            nickname = email.split('@')[0]
            user=User(nickname=username, email=email)
            session.add(user)
            session.commit()
    
    
    login_user(user, remember=True)
    return redirect(url_for('login'))

@flaskapp.route('/')
@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In')


# @flaskapp.route('/login', methods=['GET', 'POST'])
# def login():
#     form=LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         user=session.query(User).filter_by(username=form.username.data).first()
#         if user:
#                if user.usertype=="ADMIN":
#                    if user.password == form.password.data:
#                       return redirect('/list')
#                    else:
#                       return'<h1>Invalid username or password </h1>'
#                else:
#                    if user.password == form.password.data:
#                       return redirect('/search')
#                    else:
#                       return'<h1>Invalid username or password </h1>'
#         else:
#            return'<h1>Invalid username or password</h1>'
#     return render_template('login.html', form=form)

@flaskapp.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(name=form.name.data ,username=form.username.data ,email=form.email.data \
            ,password=form.password.data ,accntno= form.accntno.data ,ifsccode= form.ifsccode.data \
            ,payment_type=form.payment_type.data ,transaction_type=form.transaction_type.data,usertype=form.usertype.data)
        session.add(user)
        session.commit()
        flash('Congratulations, you are  registered successfully !')
        return redirect('/register')
            
    return render_template('register.html', title='Register', form=form)

@flaskapp.route('/search',methods=['GET' , 'POST'])
def search():
    views = session.query(User).all()
    form=SearchForm()
    if request.method =='POST':
        serc=session.query(User).filter(User.username.startswith(form.username.data)).all()
        return render_template('search.html', serc=serc, form= form)
    
    return render_template('search.html', form = form, views=views)

@flaskapp.route('/delete', methods =['GET', 'POST'])
def delete():
         if request.method == 'GET':
             del_user = session.query(User).filter_by(id=request.args.get('id')).first()
             session.delete(del_user)
             session.commit()
             flash('User has been deleted!!!')
             return redirect('/list')
@flaskapp.route('/list', methods =['GET', 'POST'])
def view():
     views = session.query(User).all()  
     return render_template('list.html', views=views)

@flaskapp.route('/views', methods =['GET', 'POST'])
def view_detail():
       item=session.query(User).filter_by(id=request.args.get('id')).all()
       return render_template('view.html', display=item)

@flaskapp.route('/update', methods =['GET', 'POST'])
def edit():
    form = UpdateForm()
    update_user= session.query(User).filter_by(id=request.args.get('id')).first()
    if update_user:
        if form.validate_on_submit():
            update_user.name = form.name.data
            update_user.username=form.username.data
            update_user.email=form.email.data
            update_user.accntno=form.accntno.data
            update_user.ifsccode=form.ifsccode.data
            update_user.payment_type=form.payment_type.data 
            update_user.transaction_type=form.transaction_type.data
            update_user.usertype=form.usertype.data
            session.commit()
            flash('successfully changed your data')
            return render_template('update.html', form=form)
        else:
            form.name.data = update_user.name    
            form.username.data = update_user.username
            form.email.data = update_user.email
            form.accntno.data = update_user.accntno
            form.ifsccode.data = update_user.ifsccode
            form.payment_type.data = update_user.payment_type
            form.transaction_type.data = update_user.transaction_type
            form.usertype.data=update_user.usertype
            return render_template('update.html', form=form)
    else:
            return render_template('update.html',form=form)
@flaskapp.route('/blogreg',methods=['GET','POST'])
def blogreg():
    form = BlogForm()
    if form.validate_on_submit():
        user=Blog(title=form.title.data ,message=form.message.data ,user_id=form.user_id.data)
        session.add(user)
        session.commit()
        flash('Congratulations, your post registered successfully !')
        return redirect('/blogreg')
            
    return render_template('blog_reg.html', title='blogreg', form=form)

@flaskapp.route('/blogview',methods=['GET','POST'])
def blogview():
    views = session.query(Blog).all()  
    return render_template('blog_view.html', views=views)

@flaskapp.route('/bloglist', methods =['GET', 'POST'])
def blogview_detail():
    item=session.query(Blog).filter_by(user_id=request.args.get('user_id')).all()
    return render_template('blog_list.html', item=item)

@flaskapp.route('/blog_delete', methods =['GET', 'POST'])
def blog_delete():
         if request.method == 'GET':
             del_user = session.query(Blog).filter_by(user_id=request.args.get('user_id')).first()
             session.delete(del_user)
             session.commit()
             flash('User has been deleted!!!')
             return redirect('/bloglist')

