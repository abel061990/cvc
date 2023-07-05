
from flask import Blueprint,render_template,redirect, url_for, request, flash,g,send_from_directory
from flask_login import login_user,logout_user,login_required
from . import db
from .create_tables.models import User
from werkzeug.security import generate_password_hash,check_password_hash
'''from flask_jwt_extended import (JWTManager, create_access_token,create_refresh_token,
                                get_jwt, jwt_required,get_jwt_identity)'''
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, jwt_refresh_token_required,
                                get_jwt_claims, jwt_required, get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)
from .forms import RegistrationForm
import datetime
from dateutil import relativedelta

main = Blueprint('main', __name__)

@main.route('/login_admin')
def login():
    return render_template('login.html')


@main.route('/process', methods=['POST'])
def login_post():
    matricule = request.form.get('username')

    password = request.form.get('password')

    #claims = get_jwt_claims()




    users = User.query.filter_by(matricule=matricule)
    passw=False
    user=None
    for u in users:
        if check_password_hash(u.mot_de_passe, password):
            user=u
            break



    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if (not user) :
        flash('S"il vous plait vérifier vos accès et ressayer encore.')
        return redirect('/login_admin')  # if user doesn't exist or password is wrong, reload the page

    else:

        login_user(user)
        return redirect('/admin')

    # if the above check passes, then we know the user has the right credentials

    return redirect('/login_admin')

@main.route('/logout')
#@jwt_required(refresh=True)
@jwt_refresh_token_required
@login_required
def logout():
    logout_user()
    return redirect('/login_admin')

@main.route('/back/change/password', methods=['GET'])
def change():
    form = RegistrationForm(request.form)
    #print(request.form)

    '''user = User(form.username.data, form.email.data,
                form.password.data)
    db_session.add(user)
    flash('Thanks for registering')'''
    #return redirect(url_for('login'))
    return render_template('password_reset.html',form=form)




@main.route('/back/submit', methods=['POST'])
def submit():
    form = RegistrationForm(request.form)
    user = User.query.filter_by(matricule=form.data['username']).first()
    if user:
        if (check_password_hash(user.mot_de_passe, form.data['old_password'])):

            if form.validate():
                user.mot_de_passe = generate_password_hash(form.data['password'], method='sha256')
                user.expire_data=datetime.datetime.utcnow+relativedelta.relativedelta(months=3)
                db.session.commit()
                db.session.close()
                return redirect('/back/success')

    return render_template('password_reset.html',form=form)

@main.route('/back/success', methods=['GET'])
def success():


    return render_template('success.html')
