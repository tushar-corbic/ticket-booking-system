from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tushar_database.sqlite3'
app.config['SECRET_KEY'] = 'tusharmeyofsecret'
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Interger, nullable=False)
    shows = db.relationship("show", back_populates = "venue")

class Show(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable =False)
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


db.create_all()

# main index 
@app.route('/')
def index():
    return render_template('index.html',title="")


#admin login
@app.route("/admin/", methods=["GET","POST"])
def adminIndex():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username=="" or password=="":
            flash("Please enter all the fields", "danger")
            return redirect("/admin/")
        else:
            admins = Admin().query.filter_by(username=username).first()
            if admins and bcrypt.check_password_hash(admins.password, password):
                session["admin_id"] = admins.id 
                session["admin_name"] = admins.username
                flash("Logined Successfully", "success")
                return redirect("/admin/dashboard")
            else:
                flash("Incorrect Credentials","danger")
                return redirect("/admin/")
    else:
        return render_template("admin/index.html", title="Admin Login")

@app.route("/admin/dashboard")
def adminDashboard():
    if not session.get("admin_id"):
        return redirect("/admin/")
    totalUser=User.query.count()
    totalApprove=User.query.filter_by(status=1).count()
    NotTotalApprove=User.query.filter_by(status=0).count()
    return render_template('admin/dashboard.html',title="Admin Dashboard",totalUser=totalUser,totalApprove=totalApprove,NotTotalApprove=NotTotalApprove)

# admin get all user 
@app.route('/admin/get-all-user', methods=["POST","GET"])
def adminGetAllUser():
    if not session.get('admin_id'):
        return redirect('/admin/')
    if request.method== "POST":
        search=request.form.get('search')
        users=User.query.filter(User.username.like('%'+search+'%')).all()
        return render_template('admin/all-user.html',title='Approve User',users=users)
    else:
        users=User.query.all()
        return render_template('admin/all-user.html',title='Approve User',users=users)

@app.route('/admin/approve-user/<int:id>')
def adminApprove(id):
    if not session.get('admin_id'):
        return redirect('/admin/')
    User().query.filter_by(id=id).update(dict(status=1))
    db.session.commit()
    flash('Approve Successfully','success')
    return redirect('/admin/get-all-user')


# change admin password
@app.route('/admin/change-admin-password',methods=["POST","GET"])
def adminChangePassword():
    # admin=Admin.query.get(1)
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        new_password = request.form.get("new_password")
        if username == "" or password=="" or new_password=="":
            flash('Please fill the field','danger')
            return redirect('/admin/change-admin-password')
        else:
            admins = Admin().query.filter_by(username=username).first()
            if admins:
                if bcrypt.check_password_hash(admins.password, password):
                    Admin().query.filter_by(username=username).update(dict(password=bcrypt.generate_password_hash(new_password,10)))
                    db.session.commit()
                    flash('Admin Password update successfully','success')
                    return redirect('/admin/change-admin-password')
                else:
                    flash("Wrong passsword ", "danger")
            else:
                flash("wrong username", "danger")
    else:
        return render_template('admin/admin-change-password.html',title='Admin Change Password')
        # return render_template('admin/admin-change-password.html',title='Admin Change Password',admin=admin)

# admin logout
@app.route('/admin/logout')
def adminLogout():
    if not session.get('admin_id'):
        return redirect('/admin/')
    if session.get('admin_id'):
        session['admin_id']=None
        session['admin_name']=None
        return redirect('/')
# -------------------------use

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
    pass
class DeleteVenueForm(FlaskForm):
    pass

class AddShowForm(FlaskForm):
    pass

class UpdateShowForm(FlaskForm):
    pass

class DeleteShowForm(FlaskForm):
    pass



# @app.route('/')
# def home():
#     return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    raise ValidationError(
                'Incorrect Password')


    # return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, 
            password=hashed_password, 
            firstname=form.firstname.data, 
            lastname =form.lastname.data,
             email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    raise ValidationError(
                'Could not Register!!! Please try again')


    return render_template('register.html', form=form)

@app.route("/addVenue", methods=["GET", "POST"])
def updateVenue():
    pass


if __name__ == "__main__":
    app.run(debug=True)