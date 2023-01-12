from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify
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
app.config['SECRET_KEY'] = 'tusharmeyofsecret'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    firstname= db.Column(db.String(40), nullable=True)
    lastname = db.Column(db.String(40), nullable=True)
    email    = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
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


########################################## api for user login ######################################3

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

        class_entry_relations = get_dropdown_values()

        default_classes = sorted(class_entry_relations.keys())
        default_values = class_entry_relations[default_classes[0]]
        addticketform = AddTicketForm()
        all_tickets = Ticket.query.filter_by(customerid=session["user_id"]).all()
        return render_template("user/dashboard.html", tickets = all_tickets, addticketform=addticketform,  all_classes=default_classes, all_entries=default_values)


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
        else:
            print("not able to register!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return render_template("user/signup.html", form = form )



@app.route("/user/change_password", methods=["POST", "GET"])
def change_password():
    if session["user_name"]!=None and session["user_id"]!=None:
        if request.method=='POST':
            username = request.form["username"]
            old_password = request.form["old_password"]
            old_user = User.query.filter_by(username=username).first()
            print(old_user, "first")
            
            # print(old_user, "---------------------------")
            if old_user!=None:
                new_password = request.form["new_password"]
                old_user = User.query.filter_by(username=username, password = bcrypt.generate_password_hash(old_password)).first()
                print(old_user, "second")
                if old_user!=None:
                    new_hashed_password = bcrypt.generate_password_hash(new_password)
                    user = User.query.filter_by(username=username).update(dict(password = new_hashed_password))
                    db.session.commit()
                    flash("Password changed successfully", "success")
                else:
                    flash("wrong password ", 'danger')
            else:
                flash("wrong username","danger")
    return render_template("user/change-password.html")

@app.route('/logout/', methods=["POST","GET"])
@login_required
def logout():
    print("asfd------------")
    if request.method=='POST':
        if session["user_id"]!=None and session["user_name"]!=None:
            session["user_id"]=None
            session["user_name"] = None
            print("logouut--------------------")
            return redirect(url_for("index"))


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


    return render_template('user/signup.html', form=form)
############################################# api for user login end ###############################33


######################### api for venue##################################################
@app.route("/admin/addVenue", methods=["GET", "POST"])
def addVenue():
    if not session.get('admin_id'):
        return redirect('/admin/')
    form = AddVenueForm()
    if form.validate_on_submit()==False:
        if Venue.query.filter_by(name=form.name.data).all()==[]:
            new_venue = Venue(name=form.name.data,place = form.place.data, capacity = form.capacity.data)
            db.session.add(new_venue)
            db.session.commit()
            flash("added the venue successfully", "success")
            return redirect("/admin/dashboard")
        else:
            flash("Venue already exist", "danger")
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
    if form.validate_on_submit()==False:
        old_venue = Venue.query.filter_by(id=form.name.data).first()
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
        if Show.query.filter_by(name=form.name.data, venue_id=form.venue.data).all()==[]:
            new_show = Show(name=form.name.data,ratings = form.ratings.data, tags = form.tags.data, ticketPrice = form.ticketPrice.data,
                            venue_id= form.venue.data)
            db.session.add(new_show)
            db.session.commit()
            flash("added the Show successfully", "success")
            return redirect("/admin/dashboard")
        else:
            flash("Show already exist", "danger")
            return redirect("/admin/dashboard")
    print("could not add the Show")
    flash("Could not add Show!!!!")
    return redirect("/admin/dashboard")


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
            flash("Did not found the Show for update", "danger")
            return redirect("/admin/dashboard")
        else:
            Show.query.filter_by(id=form.name.data).delete()
            db.session.commit()
            flash("Deleted the Show successfully", "success")
            return redirect("/admin/dashboard")



########################### api for show end ####################################################

############################ api for ticket booking #############################################
@app.route("/user/gotoaddticketpage")
def gottoaddticketpage():
    if session["user_id"]!=None and session["user_name"]!=None:
        pass
    return render_template("user/ticket.html")



@app.route("/user/addTicket/", methods=["GET", "POST"])
# @login_required
def addTicket():
    if session["user_id"]!=None and session["user_name"]!=None:
        form = AddTicketForm()
        form.venue_name.choices= [(i.id, i.name) for i in Venue.query.all()]
        if request.method=='POST':
            show_selected = Show.query.filter_by(name=request.form["showname"]).first()
            venue_selected = Venue.query.filter_by(name=request.form["venuename"]).first()
            old_ticket = Ticket.query.filter_by(showname=show_selected.name, venuename=venue_selected.name).all()
            if old_ticket==[]:
                new_ticket= Ticket(showname=show_selected.name,venuename=venue_selected.name, ticketqty=request.form["ticketqty"],customerid=session["user_id"], ticketprice = show_selected.ticketPrice )
                db.session.add(new_ticket)
                db.session.commit()
                return redirect(url_for("userDashboard"))
            else:
                flash("ticket already purchased","danger")
                return redirect(url_for("userDashboard"))
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

def get_dropdown_values():
    carbrands = Venue.query.all()
    myDict = {}
    for p in carbrands:
        key = p.name
        brand_id = p.id
        q = Show.query.filter_by(venue_id=brand_id).all()
        lst_c = []
        for c in q:
            lst_c.append( c.name )
        myDict[key] = lst_c
    class_entry_relations = myDict
    return class_entry_relations


@app.route('/_update_dropdown')
def update_dropdown():
    selected_class = request.args.get('selected_class', type=str)
    updated_values = get_dropdown_values()[selected_class]
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)
    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    return jsonify(random_text="You selected the car brand: {} and the model: {}.".format(selected_class, selected_entry))


if __name__ == "__main__":
    app.run(debug=True)