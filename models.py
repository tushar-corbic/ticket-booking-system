# from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField,SelectMultipleField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Email, NumberRange
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
    lastname= StringField(validators=[
                            InputRequired(), Length(max=40)], render_kw={"placeholder":"Last Name"})
    email= EmailField("Email Address", validators=[InputRequired(), Email()], render_kw={"placeholder":"tusharemail"})                    
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        print("validatings")
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            print("gettinga  validation error")

            raise ValidationError(
                'That username or Email already exists. Please choose a different one.')




class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class UpdateVenueForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
    place = StringField(Validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place"})
    capacity = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"Capacity"})  
    

class AddVenueForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
    place = StringField(Validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place"})
    capacity = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"Capacity"})  
    
    submit = SubmitField('Submit')

class DeleteVenueForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
    submit = SubmitField('Submit')

    def validate_venue_name(self, name):
        existing_venue_name=Venue().query.filter(name=name).first()
        if existing_venue_name=="":
            raise ValidationError("VenueName Does not exist")




class AddShowForm(FlaskForm):
    name= StringField(Validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Show Name"})
    ratings = IntegerField(Validators=[InputRequired(),  NumberRange(min=0, max=100)], render_kw={"placeholder":"Show Rating"})
    tags = SelectMultipleField(u'Movie Genre', choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), 
                                                ('Romance', 'Romance'),
                                                ('Comedy', 'Comedy')])
    ticketPrice = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"ticket price"})    
    # all_venue_id =[i.id for i in  Venue.query.all() ]
    # all_venue_name=[i.name for i in Venue.query().all()]
    all_venue_id =[ ]
    all_venue_name=[]
    venue_choices = [j for i, j in enumerate(zip(all_venue_id, all_venue_name))]                                      
    venue = SelectField(Validators=[InputRequired()], choices=venue_choices ,render_kw={"placeholder":"Venue"})
    submit = SubmitField('Submit')
    



class UpdateShowForm(FlaskForm):
    # all_shows = [i.name for i in Show().query().all()]
    # all_shows = [(i,j) for i,j in enumerate(all_shows)]
    all_shows = []
    name= SelectField(Validators=[InputRequired()],choices=all_shows ,render_kw={"placeholder":"Show Name"})
    ratings = IntegerField(Validators=[InputRequired(),  NumberRange(min=0, max=100)], render_kw={"placeholder":"Show Rating"})
    tags = SelectMultipleField(u'Movie Genre', choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), 
                                                ('Romance', 'Romance'),
                                                ('Comedy', 'Comedy')])
    ticketPrice = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"ticket price"})  
    # all_venue_id =[i.id for i in  Venue.query.all() ]
    # all_venue_name=[i.name for i in Venue.query.all()]
    all_venue_id =[ ]
    all_venue_name=[]
    venue_choices = [j for i, j in enumerate(zip(all_venue_id, all_venue_name))]                                      
    venue = SelectField(Validators=[InputRequired()], choices=venue_choices ,render_kw={"placeholder":"Venue"})
    submit = SubmitField('Login')

    def validate_show_name(self, name):
        existing_show_name = Show().query.filter(name=name).first()
        if existing_show_name=="":
            raise ValidationError("Show Name Does not exxist")


class DeleteShowForm(FlaskForm):
    # all_shows = [i.name for i in Show().query().all()]
    # all_shows = [(i,j) for i,j in enumerate(all_shows)]
    all_shows=[]
    name= SelectField(Validators=[InputRequired()],choices=all_shows ,render_kw={"placeholder":"Show Name"})
    submit = SubmitField('Login')

    def validate_show_name(self, name):
        existing_show_name = Show().query.filter(name=name).first()
        if existing_show_name=="":
            raise ValidationError("Show Name Does not exxist")


# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField,SelectMultipleField, SelectField
# from wtforms.validators import InputRequired, Length, ValidationError, Email, NumberRange


# class Venue(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False, unique=True)
#     place = db.Column(db.String(255), nullable=False)
#     capacity = db.Column(db.Interger, nullable=False)
#     # shows = db.relationship("show", back_populates = "venue")

# class Show(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(100), nullable =False, unique=True)
#     ratings = db.Column(db.Interger, nullable =False)
#     tags = db.Columns(db.String(255), nullable=False)
#     ticketPrice = db.Column(db.Integer, nullable =False)
#     venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
#     # venue = db.relationship("venue", back_populates = "show")


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     firstname= db.Column(db.String(40), nullable=True)
#     lastname = db.Column(db.String(40), nullable=True)
#     email    = db.Column(db.String(100), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)
    
#     def __repr__(self):
#         return f'User("{self.id}","{self.username},"{self.firstname}","{self.lastname}","{self.email}"'


# class Admin(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(255), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)
    
#     def __repr__(self):
#         return f'Admin("{self.username}","{self.id}")'

# class AdminLoginForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Login')



# class RegisterForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
#     firstname= StringField(validators=[
#                             InputRequired(), Length(max=40)], render_kw={"placeholder":"First Name"})
#     lastname= StringField(Validators=[
#                             InputRequired(), Length(max=40)], render_kw={"placeholder":"Last Name"})
#     email= EmailField("Email Address", validators=[InputRequired(), Email()], render_kw={"placeholder","tusharemail"})                    
#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         existing_user_username = User.query.filter(
#             username=username.data).first()
#         if existing_user_username:
#             raise ValidationError(
#                 'That username or Email already exists. Please choose a different one.')




# class LoginForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Login')

# class UpdateVenueForm(FlaskForm):
#     name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
#     place = StringField(Validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place"})
#     capacity = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"Capacity"})  
    

# class AddVenueForm(FlaskForm):
#     name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
#     place = StringField(Validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place"})
#     capacity = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"Capacity"})  
    
#     submit = SubmitField('Login')

# class DeleteVenueForm(FlaskForm):
#     name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name"})
#     submit = SubmitField('Login')

#     def validate_venue_name(self, name):
#         existing_venue_name=Venue().query.filter(name=name).first()
#         if existing_venue_name=="":
#             raise ValidationError("VenueName Does not exist")




# class AddShowForm(FlaskForm):
#     name= StringField(Validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Show Name"})
#     ratings = IntegerField(Validators=[InputRequired(),  NumberRange(min=0, max=100)], render_kw={"placeholder":"Show Rating"})
#     tags = SelectMultipleField(u'Movie Genre', choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), 
#                                                 ('Romance', 'Romance'),
#                                                 ('Comedy', 'Comedy')])
#     ticketPrice = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"ticket price"})    
#     all_venue_id =[i.id for i in  Venue().query.all() ]
#     all_venue_name=[i.name for i in Venue().query().all()]
#     venue_choices = [j for i, j in enumerate(zip(all_venue_id, all_venue_name))]                                      
#     venue = SelectField(Validators=[InputRequired()], choices=venue_choices ,render_kw={"placeholder":"Venue"})
#     submit = SubmitField('Login')



# class UpdateShowForm(FlaskForm):
#     all_shows = [i.name for i in Show().query().all()]
#     all_shows = [(i,j) for i,j in enumerate(all_shows)]

#     name= SelectField(Validators=[InputRequired()],choices=all_shows ,render_kw={"placeholder":"Show Name"})
#     ratings = IntegerField(Validators=[InputRequired(),  NumberRange(min=0, max=100)], render_kw={"placeholder":"Show Rating"})
#     tags = SelectMultipleField(u'Movie Genre', choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), 
#                                                 ('Romance', 'Romance'),
#                                                 ('Comedy', 'Comedy')])
#     ticketPrice = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"ticket price"})  
#     all_venue_id =[i.id for i in  Venue().query.all() ]
#     all_venue_name=[i.name for i in Venue().query().all()]
#     venue_choices = [j for i, j in enumerate(zip(all_venue_id, all_venue_name))]                                      
#     venue = SelectField(Validators=[InputRequired()], choices=venue_choices ,render_kw={"placeholder":"Venue"})
#     submit = SubmitField('Login')

#     def validate_show_name(self, name):
#         existing_show_name = Show().query.filter(name=name).first()
#         if existing_show_name=="":
#             raise ValidationError("Show Name Does not exxist")


# class DeleteShowForm(FlaskForm):
#     all_shows = [i.name for i in Show().query().all()]
#     all_shows = [(i,j) for i,j in enumerate(all_shows)]

#     name= SelectField(Validators=[InputRequired()],choices=all_shows ,render_kw={"placeholder":"Show Name"})
#     submit = SubmitField('Login')

#     def validate_show_name(self, name):
#         existing_show_name = Show().query.filter(name=name).first()
#         if existing_show_name=="":
#             raise ValidationError("Show Name Does not exxist")

