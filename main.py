import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from app_functions import create_token, send_email
from flask import Flask
from itsdangerous import URLSafeTimedSerializer



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("PASSMANAGER_SECRET_KEY")
# app.secret_key = 'this-is-my-secret-key-jajaja!!!' #This is necessary for the flash() method and for flask-login
# app.config['SECRET_KEY'] = 'this-is-my-secret-key-jajaja!!!'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


#****************** CRYPTOGRAPHY CONFIGURATION *******************#

# secret_key = Fernet.generate_key()
# cipher_suite = Fernet(secret_key)


#****************** FLASK-LOGIN CONFIGURATION *******************#

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.fname = user_data['fname']
        self.lname = user_data['lname']
        self.email = user_data['email']
        self.password = user_data['password']
    
    def get_id(self):
        return self.id
    
    @staticmethod
    def find_user(email):
        user_data = users_col.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None
    
    @staticmethod
    def find_user_id(user_id):
        user_data = users_col.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.find_user_id(user_id)


#****************** CONNECT WITH MONGO CLIENT *******************#

db_password = os.environ.get("DB_PASSWORD")
uri = "mongodb+srv://projectsmiltonix:<" + db_password + ">@cluster0.970wx6j.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client['passManagerDB'] #another option is client.userDB
users_col = db['users'] #another option is db.users
credentials_col = db.credentials

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#****************** FUNCTIONS *******************#

def get_credential_info():
    name = request.form.get('name_input')
    username = request.form.get('username_input')
    password = request.form.get('password_input')
    user_id = current_user.id
    
    credential_info = {
        'name': name,
        'username': username,
        'password': password,
        'user_id': user_id,
    }
    return credential_info

def decrypt_password(record):
    encrypted_pass = record['password']
    decrypted_pass = serializer.loads(encrypted_pass)
    record['password'] = decrypted_pass
    return record
    

#****************** ROUTES *******************#

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':

        if User.find_user(request.form.get('email_input')):
            flash("You've aldeady signed up with that email, log in instead!")
            return redirect(url_for('login'))

        new_user = {
            'fname': request.form.get('first_name_input'),
            'lname': request.form.get('last_name_input'),
            'email': request.form.get('email_input'),
            'password': generate_password_hash(request.form.get('password_input'), method='pbkdf2:sha256', salt_length=8),
        }

        users_col.insert_one(new_user)
        new_user_class = User(new_user)
        print(new_user_class.email)

        login_user(new_user_class)
        
        # flash("Your account has been created. Please login.")
        return redirect(url_for('my_records'))

    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_records'))
    
    if request.method == "POST":
        email = request.form.get('email_input')
        password = request.form.get('password_input')

        user = User.find_user(email)

        if user == None:
            flash("The email does not exist. Please try again.")
            return redirect(url_for('login'))
        
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('my_records'))
            
            else:
                flash('Password incorrect. Try again')
                return redirect(url_for('login'))


    return render_template("login.html")


@app.route('/new-record', methods=["GET", "POST"])
@login_required
def create_record():
    if request.method == 'POST':
        name = request.form.get('name_input')
        username = request.form.get('username_input')
        password = serializer.dumps(request.form.get('password_input'))
        user_id = current_user.id
        
        credential_info = {
            'name': name,
            'username': username,
            'password': password,
            'user_id': user_id,
        }

        credentials_col.insert_one(credential_info)

        return redirect(url_for('my_records'))

    return render_template("create_record.html", is_authenticated=True, user=current_user)


@app.route('/delete-record', methods=["GET", "POST"])
@login_required
def delete_record():
    
    record_id = request.form.get('record_id')[6:]
    record_to_delete = credentials_col.delete_one({'_id': ObjectId(record_id)})
    
    if record_to_delete.deleted_count > 0:
        flash('Record deleted successfully.')

    return jsonify({'redirect_url': url_for('my_records')})


@app.route('/update-record/<record_id>', methods=["GET", "POST"])
@login_required
def edit_record(record_id):
    record_to_edit = credentials_col.find_one({'_id': ObjectId(record_id)})
    record_decrypted = decrypt_password(record_to_edit)

    if request.method == 'POST':
        credential_info = get_credential_info()
        print(credential_info)
        credential_info['password'] = serializer.dumps(credential_info['password'])
        print(credential_info)
        credentials_col.update_one({'_id': ObjectId(record_id)},
                                   {'$set': credential_info}
                                   )
        
        return redirect(url_for('my_records'))

    return render_template("create_record.html", is_authenticated=True, user=current_user, editing=True, record=record_decrypted)
    


@app.route('/my-records')
@login_required
def my_records():
    all_records = credentials_col.find({'user_id': current_user.id})
    encrypted_records = []
    for record in all_records:
        record = decrypt_password(record)
        encrypted_records.append(record)
    return render_template("my_records.html", all_records=encrypted_records, is_authenticated=True, user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/reset-password', methods=["GET", "POST"])
def reset_password():
    if request.method == 'POST':
        recovery_email = request.form.get('email_input')
        email_found = users_col.find_one({'email': recovery_email})
        print(email_found)
        if email_found:
            token = create_token()
            link = 'http://127.0.0.1:5000/update-user/' + token
            send_email(recovery_email, link)

            users_col.update_one({'email': recovery_email},
                                 {'$set': {'token': token}}
                                 )
            
            return "The link was sent to your email."
        
        else:
            flash("The email was not found, please try again or sign up to create an account.")
            return redirect(url_for("reset_password"))
        
    return render_template('/reset-password.html')


@app.route('/update-user/<token>', methods=["GET", "POST"])
def update_user(token):
    if request.method == 'POST':
        user_email = request.form.get('email_input')
        new_pass = generate_password_hash(request.form.get('new_pass_input'), method='pbkdf2:sha256', salt_length=8)
        
        user_to_update = users_col.find_one({'token': token, 'email': user_email})
        print(user_to_update)

        if user_to_update:
            users_col.update_one({'token': token, 'email': user_email},
                                                {'$set': {'password': new_pass}})
            flash("Your password have been changed sucessfully. Please login.")
            return redirect(url_for('login'))
        
        else:
            flash("This link is not longer available or the email you enter is not in our database. Please correct your email or ask for a new link.")
            return redirect(url_for('update_user', token=token))
            
    return render_template('/change-password.html', token=token)


if __name__ == "__main__":
    app.run(debug=False)