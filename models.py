from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField,SelectMultipleField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Email, NumberRange
class AdminLoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username","class":"form-control my-1"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password","class":"form-control my-1"})

    submit = SubmitField('Login', render_kw={"class":"btn btn-success"})


# ading contirubtuio fo the new amoooit 
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username","class":"form-control my-1 "})
    firstname= StringField(validators=[
                            InputRequired(), Length(max=40)], render_kw={"placeholder":"First Name","class":"form-control my-1 "})
    lastname= StringField(validators=[
                            InputRequired(), Length(max=40)], render_kw={"placeholder":"Last Name","class":"form-control my-1 "})
    email= EmailField("Email Address", validators=[InputRequired(), Email()], render_kw={"placeholder":"tusharemail","class":"form-control my-1 "})                    
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password","class":"form-control my-1 "})

    submit = SubmitField('Register', render_kw={"class":"btn btn-success"})



class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username","class":"form-control my-1 "})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password","class":"form-control my-1 "})

    submit = SubmitField('Login', render_kw={"class":"btn btn-success"})

class UpdateVenueForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name","class":"form-control my-1 "})
    place = StringField(Validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place","class":"form-control my-1 "})
    capacity = IntegerField(Validators=[InputRequired()], render_kw={"placeholder":"Capacity","class":"form-control my-1 "})  
    

class AddVenueForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name","class":"form-control my-1 "})
    place = StringField(validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder":"Venue Place","class":"form-control my-1 "})
    capacity = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"Capacity","class":"form-control my-1 "})  
    
    submit = SubmitField('Submit', render_kw={"class":"btn btn-success"})

class DeleteVenueForm(FlaskForm):
    name= SelectField(validators=[InputRequired()], choices = [],render_kw={"placeholder":"Venue Name","class":"form-control my-1 "})
    # name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Venue Name","class":"form-control my-1 "})
    submit = SubmitField('Delete', render_kw={"class":"btn btn-danger"})

    def validate_venue_name(self, name):
        existing_venue_name=Venue.query.filter(name=name).first()
        if existing_venue_name=="":
            raise ValidationError("VenueName Does not exist")




class AddShowForm(FlaskForm):
    name= StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder":"Show Name","class":"form-control my-1 "})
    ratings = IntegerField(validators=[InputRequired(),  NumberRange(min=0, max=100)], render_kw={"placeholder":"Show Rating","class":"form-control my-1 "})
    tags = SelectField(u'Movie Genre', choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), 
                                                ('Romance', 'Romance'),
                                                ('Comedy', 'Comedy')])
    ticketPrice = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"ticket price","class":"form-control my-1 "})    
    venue = SelectField(validators=[InputRequired()], choices=[] ,render_kw={"placeholder":"Venue","class":"form-control my-1 "})
    submit = SubmitField('Submit', render_kw={"class":"btn btn-success"})
    



class UpdateShowForm(FlaskForm):
    all_shows = []
    name= SelectField(validators=[InputRequired()],choices=all_shows ,render_kw={"placeholder":"Show Name","class":"form-control my-1 "})
    ratings = IntegerField(validators=[InputRequired(),  NumberRange(min=0, max=100)], render_kw={"placeholder":"Show Rating","class":"form-control my-1 "})
    tags = SelectMultipleField(u'Movie Genre', choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), 
                                                ('Romance', 'Romance'),
                                                ('Comedy', 'Comedy')])
    ticketPrice = IntegerField(validators=[InputRequired()], render_kw={"placeholder":"ticket price","class":"form-control my-1 "})  
    all_venue_id =[ ]
    all_venue_name=[]
    venue_choices = [j for i, j in enumerate(zip(all_venue_id, all_venue_name))]                                      
    venue = SelectField(validators=[InputRequired()], choices=venue_choices ,render_kw={"placeholder":"Venue","class":"form-control my-1 "})
    submit = SubmitField('Login', render_kw={"class":"btn btn-success"})

    def validate_show_name(self, name):
        existing_show_name = Show().query.filter(name=name).first()
        if existing_show_name=="":
            raise ValidationError("Show Name Does not exxist")


class DeleteShowForm(FlaskForm):
    all_shows=[]
    name= SelectField(validators=[InputRequired()],choices=all_shows ,render_kw={"placeholder":"Show Name","class":"form-control my-1 "})
    submit = SubmitField('Delete', render_kw={"placeholder":"Delete ","class":"btn btn-danger form-control my-1"})

    # def validate_show_name(self, name):
    #     existing_show_name = Show().query.filter(name=name).first()
    #     if existing_show_name=="":
    #         raise ValidationError("Show Name Does not exxist")

class AddTicketForm(FlaskForm):
    venue_name = SelectField( choices = [], render_kw = {"placeholder":"Venue names","class":"form-control my-1 "})
    show_name = SelectField( choices=[], render_kw = {"placeholder":"Show name","class":"form-control my-1 "})
    ticketqty = IntegerField( render_kw = {"placeholder":"Ticket Qty", "class":"form-control my-1 "})
    submit = SubmitField("submit", render_kw={"class":"btn btn-success"})
