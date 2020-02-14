import pytest
from flaskapp import create_app
from app.models import Role, User, Permission

#https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/


@pytest.fixture(scope='module')
def new_user():
    app = create_app('testing')
    app.app_context().push()
    role_user = Role(name='User', default=True, permissions=Permission.USER)
    user = User(username='jr10', first_name='Juan Roman', last_name='Riquelme')

def test_sample(new_user):
    assert role_user.name == 'User'
    assert user.username == 'jr10'
