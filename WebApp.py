from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'accounts'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'

db = SQLAlchemy(app)
mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id, username, email, role=None):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role
        
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    options = db.Column(db.JSON, nullable=False)

    @staticmethod
    def create_form(title, questions, teacher_id):
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO forms (title, questions, teacher_id) VALUES (%s, %s, %s)', (title, questions, teacher_id))
        mysql.connection.commit()
        form_id = cursor.lastrowid
        cursor.close()
        return form_id

    @staticmethod
    def get_forms_for_teacher(teacher_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, title, questions FROM forms WHERE teacher_id = %s', (teacher_id,))
        forms_data = cursor.fetchall()
        cursor.close()
        forms = [Form(id, title, questions, teacher_id) for id, title, questions in forms_data]
        return forms
    
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, username, email, role FROM users WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User(*user_data)  
    return None

@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, email FROM teachers WHERE username = %s AND password = %s', (username, password))
        teacher_data = cursor.fetchone()
        cursor.close()

        if teacher_data:
            teacher = User(teacher_data[0], teacher_data[1], teacher_data[2])
            login_user(teacher)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('teacher_login.html')

@app.route('/index')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('teacher_index'))
        else:
            return redirect(url_for('user_index'))
    return render_template('index.html')

@app.route('/user_index')
def user_index():
    forms = None
    if current_user.role != 'teacher':
        forms = Form.get_forms_for_teacher(current_user.id)
    return render_template('user_index.html', forms=forms)

@app.route('/teacher_index')
@login_required
def teacher_index():
    return render_template('teacher_index.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, email FROM users WHERE username = %s AND password = %s', (username, password))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        role = 'user'

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_email = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        elif existing_email:
            flash('Email already exists. Please use a different one.', 'error')
            return redirect(url_for('register'))
        else:
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            cursor.execute('INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)', (username, hashed_password, email, role))
            mysql.connection.commit()
            cursor.close()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/create_form', methods=['GET', 'POST'])
@login_required
def create_form():
    form = CreateFormForm()
    if form.validate_on_submit():
        title = form.title.data
        options = [option['value'] for option in form.options.data]

        new_form = Form(title=title, options=options)
        db.session.add(new_form)
        db.session.commit()

        flash('Form created successfully!', 'success')
        return redirect(url_for('user_index'))
    
    return render_template('create_form.html', form=form)



@app.route('/forgotpassword', methods =['GET', 'POST'])
def forgotpassword():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        newpassword = request.form['newpassword']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE login SET password='"+newpassword+"' WHERE username='"+username+"' AND password='"+password+"' ")
        mysql.connection.commit()
        return render_template('index.html', msg = msg)
    else:
        return render_template('forgotpassword.html', msg = msg)
    
@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json  
    form_id = data['formId']
    rating = data['rating']
    return jsonify({'message': 'Rating submitted successfully'}), 200


# Run the application
if __name__ == '__main__':
    app.run(debug=True)