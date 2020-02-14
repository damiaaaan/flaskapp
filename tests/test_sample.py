import pytest
from flaskapp import create_app

def test_config():
    assert create_app('testing').testing

def test_def():
    assert 1==1
