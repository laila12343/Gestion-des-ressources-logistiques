import sys
import os

# Ajouter le chemin du dossier 'src' au PYTHONPATH
base_dir = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(base_dir, 'src')
sys.path.append(src_path)

from flask import Flask, render_template, request, redirect
from src.backend.analysis import plot_sales_trends
from src.backend.returns import add_return, get_all_returns
from flask import session, url_for


principal = Flask(__name__)

# Vérification du rôle "admin"
def admin_required(func):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':  # Vérifie si l'utilisateur est admin
            return redirect(url_for('login'))  # Redirige vers la page de connexion
        return func(*args, **kwargs)
    return wrapper

@principal.route('/')
@admin_required
def index():
    plot_sales_trends()
    return render_template('index.html')

@principal.route('/returns', methods=['GET', 'POST'])
@admin_required
def returns():
    if request.method == 'POST':
        product = request.form['product']
        reason = request.form['reason']
        status = request.form['status']
        option = request.form['option']
        add_return(product, reason, status, option)
        return redirect('/returns')
    returns = get_all_returns()
    return render_template('returns.html', returns=returns)

if __name__ == '_main_':
    principal.run(debug=True)