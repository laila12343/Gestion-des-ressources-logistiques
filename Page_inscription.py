from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'votre_secret_key'

# Configurer la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'votre_mot_de_passe'
app.config['MYSQL_DB'] = 'vente_en_ligne'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'mot_de_passe' in request.form and 'type' in request.form:
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        user_type = request.form['type']

        table = ''
        if user_type == 'admin':
            table = 'admin'
        elif user_type == 'livreur':
            table = 'livreurs'
        else:
            table = 'clients'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM {table} WHERE email = %s AND mot_de_passe = %s', (email, mot_de_passe,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['type'] = user_type
            return redirect(url_for(f'{user_type}_home'))
        else:
            msg = 'Identifiant ou mot de passe incorrect !'

    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'mot_de_passe' in request.form and 'nom' in request.form and 'type' in request.form:
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        user_type = request.form['type']

        table = ''
        if user_type == 'admin':
            table = 'admin'
        elif user_type == 'livreur':
            table = 'livreurs'
        else:
            table = 'clients'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM {table} WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            msg = 'Le compte existe déjà !'
        else:
            cursor.execute(f'INSERT INTO {table} (nom, email, mot_de_passe) VALUES (%s, %s, %s)', (nom, email, mot_de_passe,))
            mysql.connection.commit()
            msg = 'Vous êtes enregistré avec succès !'

    return render_template('register.html', msg=msg)

# Page pour les administrateurs
@app.route('/admin_home')
def admin_home():
    if 'loggedin' in session and session['type'] == 'admin':
        return f"Bienvenue Admin {session['email']}"
    return redirect(url_for('login'))

# Page pour les livreurs
@app.route('/livreur_home')
def livreur_home():
    if 'loggedin' in session and session['type'] == 'livreur':
        return f"Bienvenue Livreur {session['email']}"
    return redirect(url_for('login'))

# Page pour les clients
@app.route('/client_home')
def client_home():
    if 'loggedin' in session and session['type'] == 'client':
        return f"Bienvenue Client {session['email']}"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
