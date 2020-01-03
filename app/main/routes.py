from flask import redirect, request, render_template, flash, url_for, make_response, send_from_directory
from app.main import bp
from flask_login import current_user, login_required
from app import db, avatars
from app.models import User
from app.main.forms import EditProfileForm
from werkzeug import secure_filename
import os
import tempfile
import shutil
from config import Config

projet_dir = os.environ.get('ROOT_DIR')
upload_temp_dir = os.environ.get('UPLOAD_TEMP_DIR')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Index')


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        tmp_dir = os.path.join(upload_temp_dir, request.form.get('avatar'))
        tmp_file = os.listdir(tmp_dir)[0]
        shutil.move(os.path.join(tmp_dir, tmp_file), os.path.join(Config.UPLOADED_AVATARS_DEST, tmp_file))
        os.rmdir(tmp_dir)
        current_user.avatar = tmp_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)


# uploaded data processing server for filepond javascript
@bp.route('/upload', methods=['POST'])
def upload():
    if request.files['avatar']:
        file = request.files['avatar']
        filename = secure_filename(file.filename)
        #temp_dir = tempfile.TemporaryDirectory(dir=os.environ.get('UPLOAD_DIR'))
        temp_dir = tempfile.mkdtemp(dir=upload_temp_dir)
        try:
            file.save(os.path.join(temp_dir, filename))
        except:
            flash('Error uploading the image.')
        response = make_response(str(temp_dir.split('/')[-1]), 200)
        response.mimetype = "text/plain"
        return response



@bp.route('/delete', methods=['DELETE'])
def delete():
    temp_dir = request.get_data(as_text=True)
    shutil.rmtree(os.path.join(upload_temp_dir, temp_dir)) #Remueve el directorio con el archivo
    return make_response()


@bp.route('/load', methods=['GET', 'POST'])
def load():
    ## TODO:
    #response = make_response(send_file(mp3_filepath)) o send_from_directory probar los dos
    #response.headers['X-Something'] = 'header value goes here'
    #return response
    response = make_response()
    if current_user.avatar:
        response.headers.set('Content-Disposition', 'inline')
        response.headers.set('filename', current_user.avatar)
    return response
