from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, UserMixin,login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hvcjvw822vjvj@bdbh88-ji!jvvxj"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.__init__(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    contact_no = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user)


@app.route("/courses")
def courses():
    return render_template("courses.html", logged_in=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in=current_user)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_exist = User.query.filter_by(email=request.form['email']).first()
        if not user_exist:
            user = User(
                    name=request.form['name'],
                    email=request.form['email'],
                    contact_no=request.form['contact'],
                    password=generate_password_hash(request.form['password'])
                    )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('User already exist. Try to Log In')
    return render_template("register.html", logged_in=current_user)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_exist = User.query.filter_by(email=request.form['email']).first()
        if user_exist:
            user_pass = user_exist.password
            is_correct_pass = check_password_hash(user_pass, request.form['password'])
            if is_correct_pass:
                login_user(user_exist)
                return redirect(url_for('home'))
            else:
                flash("Incorrect Password. Try Again")
        else:
            flash('User does not exist. Try to Register')
    return render_template("login.html", logged_in=current_user)


@login_required
@app.route('/logout')
def logout():
    if current_user:
        logout_user()
    return redirect(url_for('home'))


@app.route("/courses/course-<id>")
def show_course(id):
    return render_template(f"course_pages/Course-{id}.html", logged_in=current_user)


if __name__ == "__main__":
    app.run(debug=True)