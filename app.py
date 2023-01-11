from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt


import os
from models import AdminLoginForm, LoginForm, RegisterForm, AddVenueForm, AddShowForm, UpdateShowForm, UpdateVenueForm, DeleteShowForm, DeleteVenueForm, AddTicketForm
app = Flask(__name__)
bcrypt = Bcrypt(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
#  'sqlite:///tushar_database.sqlite3'
app.config['SECRET_KEY'] = 'tusharmeyofsecret'
db = SQLAlchemy(app)



# from sqlalchemy import MetaData
# metadata = MetaData()
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()
# engine = create_engine("sqlite:///test.db")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




# db.create_all()
@app.before_first_request
def create_tables():
    db.create_all()


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    place = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, place, capacity):
        self.name = name
        self.place = place
        self.capacity = capacity
    # shows = db.relationship("show", back_populates = "venue")

class Show(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable =False, unique=True)
    ratings = db.Column(db.Integer, nullable =False)
    tags = db.Column(db.String(255), nullable=False)
    ticketPrice = db.Column(db.Integer, nullable =False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)

    def __init__(self, name, ratings, tags, ticketPrice, venue_id):
        self.name= name
        self.ratings = ratings
        self.tags = tags
        self.ticketPrice = ticketPrice
        self.venue_id = venue_id
    # venue = db.relationship("venue", back_populates = "show")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    firstname= db.Column(db.String(40), nullable=True)
    lastname = db.Column(db.String(40), nullable=True)
    email    = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    def __init__(self, username, firstname, lastname, email, password):
        self.username =username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def __repr__(self):
        return f'User("{self.id}","{self.username},"{self.firstname}","{self.lastname}","{self.email}"'


class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'Admin("{self.username}","{self.id}")'
class Ticket(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    showname = db.Column(db.String(100), nullable =False)
    venuename = db.Column(db.String(100), nullable=False)
    ticketprice = db.Column(db.Integer, nullable =False)
    ticketqty = db.Column(db.Integer, nullable=False)
    customerid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
# metadata.create_all(engine)
# Base.metadata.create_all(engine)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# main index 
@app.route('/')
def index():
    return render_template('index.html',title="")

################################# api for admin login##############################################3
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
            # hashVar =bcrypt.generate_password_hash(password)
            # print(hashVar,"------------------------")
            admins = Admin.query.filter_by(username=username).first()

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
    # totalUser=User.query.count()
    # totalApprove=User.query.filter_by(status=1).count()
    # NotTotalApprove=User.query.filter_by(status=0).count()
    addvenueform = AddVenueForm()
    removevenueform = DeleteVenueForm()
    addshowform = AddShowForm()
    removeshowform = DeleteShowForm()
    all_venue = [(i.id, i.name) for i in Venue.query.all()]
    removevenueform.name.choices = all_venue
    addshowform.venue.choices = all_venue
    removeshowform.name.choices = [(i.id, i.name) for i in Show.query.all()]
    return render_template('admin/dashboard.html',title="Admin Dashboard",addvenueform = addvenueform, removevenueform = removevenueform, addshowform=addshowform, removeshowform=removeshowform)

# admin get all user 
@app.route('/admin/get-all-user', methods=["POST","GET"])
def adminGetAllUser():
    if not session.get('admin_id'):
        return redirect('/admin/')
    if request.method== "POST":
        search=request.form.get('search')
        users = User.query.all()
        # users=User.query.filter(User.username.like('%'+search+'%')).all()
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
######################################### api for admin login end ####################################


# @app.route('/')
# def home():
#     return render_template('home.html')

########################################## api for user login ######################################3
# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()

#     if request.method=='POST':
#         if form.validate_on_submit():
#             user = User.query.filter_by(username=form.username.data).first()
#             if user:
#                 if bcrypt.check_password_hash(user.password, form.password.data):
#                     login_user(user)
#                     return redirect(url_for('dashboard'))
#         # raise ValidationError(
#         #             'Incorrect Password')
#         flash("Incorrect Password ", "danger")


#     return render_template('login.html', form=form)

@app.route("/loginindex/", methods=["GET", "POST"])
def loginpage():
    form = LoginForm()

    if request.method=='POST':
        if form.validate_on_submit()==False:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    session["user_id"] = user.id
                    session["user_name"] = user.username
                    # login_user(user)
                    return redirect("/user/dashboard")
        flash("Incorrect Password ", "danger")


    return render_template("user/index.html", form = form)

@app.route("/user/dashboard")
def userDashboard():
    if session["user_id"]!=None and session["user_name"]!=None:
        all_tickets = Ticket.query.filter_by(customerid=session["user_id"]).all()
        return render_template("user/dashboard.html", tickets = all_tickets)
@app.route("/adminindex/", methods=["GET", "POST"])
def adminindex():
    return render_template("admin/index.html")


@app.route("/signupindex/", methods=["GET", "POST"])
def signupindex():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit()==False:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, 
                password=hashed_password, 
                firstname=form.firstname.data, 
                lastname =form.lastname.data,
                email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("loginpage"))
            # return redirect("user/login.html")
        else:
            print("not able to register!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return render_template("user/signup.html", form = form )
# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():

#     return render_template('dashboard.html')


@app.route('/logout/', methods=["POST","GET"])
@login_required
def logout():
    print("asfd------------")
    if request.method=='POST':
        if session["user_id"]!=None and session["user_name"]!=None:
            session["user_id"]=None
            session["user_name"] = None
            # logout_user()
            print("logouut--------------------")
            return redirect(url_for("index"))
            # return redirect("/")


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
    # raise ValidationError(
    #             'Could not Register!!! Please try again')


    return render_template('user/signup.html', form=form)
############################################# api for user login end ###############################33


######################### api for venue##################################################
@app.route("/admin/addVenue", methods=["GET", "POST"])
def addVenue():
    if not session.get('admin_id'):
        return redirect('/admin/')
    form = AddVenueForm()
    if form.validate_on_submit()==False:
        new_venue = Venue(name=form.name.data,place = form.place.data, capacity = form.capacity.data)
        db.session.add(new_venue)
        db.session.commit()
        flash("added the venue successfully", "success")
        return redirect("/admin/dashboard")
    print("could not add the venue")
    raise ValidationError("Could not add Venue!!!!")

@app.route("/admin/updateVenue", methods=["GET", "POST"])
def updateVenue():
    if not session.get("admin_id"):
        return redirect("/admin/")
    form = UpdateVenueForm()
    if form.validate_on_submit():
        old_venue = Venue().query.filter_by(name=form.name.data).first()
        if old_venue=="":
            print("did not find the venue")
            flash("Did not found the venue for update")
        else:
            Venue().query.filter_by(name=form.name.data).update(dict(place=form.place.data, capacity= form.capacity.data))
            db.session.commit()
            flash("updated the Venue successfully", "success")
            print("udpated the venue successfully")
            return redirect("/admin/")


@app.route("/admin/deleteVenue", methods=["GET" , "POST"])
def deleteVenue():
    if not session.get("admin_id"):
        return redirect("/admin/")
    form = DeleteVenueForm()
    # all_venue = [(i.id, i.name) for i in Venue.query().all()]
    # form.name.choices = all_venue
    if form.validate_on_submit()==False:
        print(form.name.data,"-----------------------------")
        old_venue = Venue.query.filter_by(id=form.name.data).first()
        print(Venue.query.all())
        print(old_venue,"----------------------------")
        if old_venue=="":
            print("did not find the venue")
            flash("Did not found the venue for update", "danger")
            return render_template("admin/dashboard.html")
        else:
            Venue.query.filter_by(id=form.name.data).delete()
            db.session.commit()
            print("deleted the venue successfully")
            flash("Deleted the venue successfully", "success")
            return redirect("/admin/dashboard")

####################### api for venue end ########################################################3




######################## api for show ############################################################
@app.route("/admin/addShow", methods=["GET", "POST"])
def addShow():
    if not session.get('admin_id'):
        return redirect('/admin/')
    form = AddShowForm()
    all_venue = [(i.id, i.name) for i in Venue.query.all()]
    form.venue.choices = all_venue
    if form.validate_on_submit()==False:
        new_show = Show(name=form.name.data,ratings = form.ratings.data, tags = form.tags.data, ticketPrice = form.ticketPrice.data,
                        venue_id= form.venue.data)
        db.session.add(new_show)
        db.session.commit()
        flash("added the Show successfully", "success")
        return redirect("/admin/dashboard")
    print("could not add the Show")
    flash("Could not add Show!!!!")
    return redirect("/admin/dashboard")

    # raise ValidationError("Could not add Show!!!!")

@app.route("/admin/updateShow", methods=["GET", "POST"])
def updateShow():
    if not session.get("admin_id"):
        return redirect("/admin/")
    form = UpdateShowForm()
    all_venue = [(i.id, i.name) for i in Venue.query().all()]
    form.venue.choices = all_venue
    if form.validate_on_submit():
        old_show = Show().query.filter_by(name=form.name.data).first()
        if old_show=="":
            print("did not find the Show")
            flash("Did not found the Show for update", "danger")
        else:
            Show().query.filter_by(name=form.name.data).update(dict(ratings=form.ratings.data, tags= form.tags.data, ticketPrice=form.ticketPrice.data,venue=form.venue.data))
            db.session.commit()
            flash("updated the Show successfully", "success")
            print("udpated the Show successfully")
            return redirect("/admin/")


@app.route("/admin/deleteShow", methods=["GET" , "POST"])
def deleteShow():
    if not session.get("admin_id"):
        return redirect("/admin/")
    form = DeleteShowForm()
    all_show = [(i.id, i.name) for i in Show.query.all()]
    form.name.choices = all_show
    if form.validate_on_submit()==False:
        old_show = Show.query.filter_by(id=form.name.data).first()
        if old_show=="":
            # print("did not find the Show")
            flash("Did not found the Show for update", "danger")
            return redirect("/admin/dashboard")
        else:
            Show.query.filter_by(id=form.name.data).delete()
            db.session.commit()
            # print("deleted the Shoe successfully")
            flash("Deleted the Show successfully", "success")
            return redirect("/admin/dashboard")



########################### api for show end ####################################################

############################ api for ticket booking #############################################
@app.route("/user/gotoaddticketpage")
def gottoaddticketpage():
    if session["user_id"]!=None and session["user_name"]!=None:
        form = AddTicketForm()
        form.show_name.choices = [(i.id, i.name) for i in Show.query.all()]
        form.venue_name.choices= [(i.id, i.name) for i in Venue.query.all()]
        return render_template("user/ticket.html", form = form)


@app.route("/user/addTicket/", methods=["GET", "POST"])
# @login_required
def addTicket():
    if session["user_id"]!=None and session["user_name"]!=None:
        form = AddTicketForm()
        # form.show_name.choices = [(i.id, i.name) for i in Show.query.all()]
        # form.venue_name.choices= [(i.id, i.name) for i in Venue.query.all()]
        # if request.method=='POST':
        if form.validate_on_submit():
            selected_venue_name = form.venue_name.data
            form.show_name.choices = [(i.id,i.name) for i in Show.query.filter_by(venue_id=selected_venue_name).all()]
            print("---------------------------------------------")
            print([(i.id,i.name) for i in Show.query.filter_by(venue_id=selected_venue_name).all()])
            selected_show_name = form.show_name.data
            selected_show = Show.query.filter_by(name=selected_show_name).first()
            new_ticket= Ticket(showname=selected_show_name,venuename=selected_venue_name, ticketqty=form.ticketqty.data,customerid=session["user_id"], ticketprice = selected_show.ticketPrice )
            db.session.add(new_ticket)
            db.session.commit()
            return redirect(url_for("userDashboard"))
        elif request.method=='GET':
            return redirect("/user/ticket.html")
        return redirect(url_for("userDashboard"))
    else:
            return redirect("/")
    


@app.route("/user/deleteTicket")
@login_required
def deleteTicket():
    pass


@app.route("/user/listTickets")
@login_required
def listTickets():
    if session["user_id"]!=None and session["user_name"]!=None:
        all_tickets = Ticket.query.filter_by(customerid = session["user_id"]).all()
        return render_template("/user/tickets.html", tickets = all_tickets)
    pass

############################# api for ticket booking end ########################################
if __name__ == "__main__":
    app.run(debug=True)