from flask import redirect, request, render_template, flash, url_for
from app.main import bp
from flask_login import current_user, login_required
from app import db, avatars
from app.models import User
from app.main.forms import EditProfileForm
from werkzeug import secure_filename


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Index')


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        
        if request.files:
            print(request.files["avatar"])
            filename = avatars.save(request.files["avatar"])
            current_user.avatar = filename
        else:
            print('NO HAY IMAGEN')
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
