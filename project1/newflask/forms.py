from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField , validators,SelectField ,IntegerField ,HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo ,Length 
from newflask.models import User ,Blog


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    accntno= StringField('AccNo', validators=[DataRequired() ,Length(min=5, max=10)])
    ifsccode= StringField('IFSCCode', validators=[DataRequired() ,Length(min=5, max=10)])
    payment_type = SelectField('PaymentType', choices = [('Other', 'Other'), ('Employee' ,'Employee')])
    transaction_type = SelectField('TransactionType', choices = [('NEFT', 'NEFT'), ('RTGS', 'RTGS') ,('IMPS', 'IMPS')])
    password = PasswordField('Password', validators=[DataRequired() ,Length(min=5, max=10)])
    confirmpassword = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    usertype= HiddenField()
    submit = SubmitField('Register')
   
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SearchForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Search')

class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    accntno= StringField('AccNo', validators=[DataRequired(),Length(min=5, max=10)])
    ifsccode= StringField('IFSCCode', validators=[DataRequired(),Length(min=5, max=10)])
    payment_type = SelectField('PaymentType', choices = [('Other', 'Other'), ('Employee' ,'Employee')])
    transaction_type = SelectField('TransactionType', choices = [('NEFT', 'NEFT'), ('RTGS', 'RTGS') ,('IMPS', 'IMPS')])
    usertype= SelectField('Usertype', choices = [('USER', 'USER'), ('ADMIN' ,'ADMIN')])
    submit= SubmitField('Update')

class BlogForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    user_id= IntegerField('User_Id', validators=[DataRequired()])
    submit= SubmitField('Submit')
    title=StringField('Title',validators=[DataRequired()])





    
    
    

