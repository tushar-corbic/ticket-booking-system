from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField,SelectMultipleField
from wtforms.validators import InputRequired, Length, ValidationError, Email

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    place = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Interger, nullable=False)
    shows = db.relationship("show", back_populates = "venue")

class Show(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable =False, unique=True)
    ratings = db.Column(db.Interger, nullable =False)
    tags = db.Columns(db.String(255), nullable=False)
    ticketPrice = db.Column(db.Integer, nullable =False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    venue = db.relationship("venue", back_populates = "show")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    firstname= db.Column(db.String(40), nullable=True)
    lastname = db.Column(db.String(40), nullable=True)
    email    = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f'User("{self.id}","{self.username},"{self.firstname}","{self.lastname}","{self.email}"'


class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f'Admin("{self.username}","{self.id}")'

class AdminLoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    firstname= StringField(validators=[
                            InputRequired(), Length(max=40)], render_kw={"placeholder":"First Name"})
    lastname= StringField(Validators=[
                            InputRequired(), Length(max=40)], render_kw={"placeholder":"Last Name"})
    email= EmailField("Email Address", validators=[InputRequired(), Email()], render_kw={"placeholder","tusharemail"})                    
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username or Email already exists. Please choose a different one.')




class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class UpdateVenueForm(FlaskForm):
    pass

class AddVenueForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
    place = StringField(Validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place"})
    capacity = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"Capacity"})  
    tags = 
class DeleteVenueForm(FlaskForm):
    pass

class AddShowForm(FlaskForm):
    pass

class UpdateShowForm(FlaskForm):
    pass

class DeleteShowForm(FlaskForm):
    pass
