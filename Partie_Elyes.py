from flask import Flask, request, jsonify,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired
from flask import render_template
from flask_sqlalchemy import  SQLAlchemy
from datetime import  datetime
import  mysql.connector
import localstorage
from mysql.connector import  Error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import  Elyes
import datascan
from werkzeug.security import generate_password_hash, check_password_hash
from intégration_google_insight import get_page_speed_insights


def connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='python'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"erreur{e}")
        return None





#démarrage de Flask
app = Flask(__name__)

app.config['SECRET_KEY'] ='kiki2021251545422'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),unique=True,nullable=False)
    mot_de_passe = db.Column(db.String(255),nullable=False)


class Liste_URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_site = db.Column(db.String(255), unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    nom_user = db.Column(db.String(255), nullable=False)
    count_elyes = db.Column(db.String(255), nullable=False)
    count_karim = db.Column(db.String(255), nullable=False)





# Route
@app.route('/url/liste')
def list_user():
    # Utilisation de filter_by sur l'objet modèle
    user_list = Liste_URL.query.filter_by(nom_user=session['username']).all()
    return render_template("liste.html", Liste=user_list)






#route
@app.route('/url/login')
def login_user():

    return render_template("Login.html")



class ajouterLien(FlaskForm):

    nom = StringField("entrer le nom de votre site", validators=[DataRequired()])
    lien = StringField("entrer le lien à vérifier", validators=[DataRequired()])

class ajouteruser(FlaskForm):

    nomuser = StringField("entrer votre email", validators=[DataRequired()])
    password = StringField("entrer votre mot de passe", validators=[DataRequired()])



class Login(FlaskForm):

    email = StringField("entrer le votre email", validators=[DataRequired()])
    mot_de_passe = StringField("Mot de passe", validators=[DataRequired()])


def user(name, mot_de_passe):
    conn = connection()

    if conn is not None:
        try:
            cursor = conn.cursor()

            query = "SELECT email, mot_de_passe FROM user WHERE email = %s"
            cursor.execute(query, (name,))

            # Utilize fetchone() to retrieve a single row
            user_data = cursor.fetchone()

            if user_data:
                stored_password = user_data[1]  # Assuming the hashed password is in the second column
                if check_password_hash(stored_password, mot_de_passe):
                    # Passwords match, user is authenticated
                    return user_data[0]  # Return the email or user identifier
                else:
                    # Passwords do not match, user is not authenticated
                    return None
            else:
                # User not found
                return None

        except Error as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
        finally:
            cursor.close()
            conn.close()



@app.route('/lien/ajouter', methods=['GET', 'POST'])
def submit_form():
    form = ajouterLien()
    if form.validate_on_submit():
        lien = form.lien.data
        nom = form.nom.data
        count = Elyes.main(lien)
        count2 = datascan.main(lien)

        if 'username' not in session or session['username'] == "":
            return render_template('Error.html', form=form)

        else:
            nouveau_lien = Liste_URL(nom_site=nom, url=lien, nom_user=session['username'], count_elyes=str(count),
                                     count_karim=str(count2))
            db.session.add(nouveau_lien)
            db.session.commit()


            api_key = 'AIzaSyBHi93uFVrk8tQ-na69HhH3oJiuRP7q2DA'

            try:
                metrics = get_page_speed_insights(lien, api_key)
                if metrics:
                    print("First Paint:", metrics.get('First Paint'))
                    print("Largest Contentful Paint:", metrics.get('Largest Contentful Paint'))
                    print("Unload Time:", metrics.get('Unload Time'))
                    print("Time to Interactive:", metrics.get('Time to Interactive'))
                else:
                    print("Erreur lors de la récupération des métriques.")
            except Exception as e:
                print(f"Erreur lors de la récupération des métriques : {e}")

        return redirect(url_for('list_user'))
    return render_template('ajouter.html', form=form)


#route
@app.route('/adduser', methods=['GET','POST'])
def adduser():
    form =ajouteruser()
    if session['username']=="":
        return render_template('Accueil.html', form=form)
    else:
        if form.validate_on_submit():
            identifiant = form.nomuser.data
            password = form.password.data
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            newUser = User(email=identifiant, mot_de_passe=hashed_password)
            db.session.add(newUser)
            db.session.commit()
            return render_template('Accueil.html', form=form)

    return render_template('ajouterUser.html', form=form)





@app.route('/', methods=['GET','POST'])
def usertest():
    form = Login()
    email = form.email.data
    mot_de_passe = form.mot_de_passe.data
    result = user(email,mot_de_passe)
    if form.validate_on_submit():
        if result:

            user2= session['username'] = email

            return render_template('Accueil.html', form=form)
        else:
            return render_template('Login.html', form=form)
    user2 = session['username'] = ""

    return render_template('Login.html', form=form)

with app.app_context():
    db.create_all()

#démaragge
if __name__ == '__main__':
    app.run(debug=True)