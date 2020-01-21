from flask import Request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, Email, Regexp
from app.models import User, Role


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    avatar = FileField('Avatar')
    submit = SubmitField('Submit')

    def __init__(self, current_user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = current_user.username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    first_name = StringField('First Name', validators=[DataRequired(), Length(3, 64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(3, 64)])
    submit = SubmitField('Submit')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                                for role in Role.query.order_by(Role.name).all()]
        self.user = user
