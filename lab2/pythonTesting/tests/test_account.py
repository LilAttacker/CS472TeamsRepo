"""
Test Cases TestAccountModel
"""
import json
from random import randrange
import pytest
from models import db, app
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  T E S T   C A S E S
######################################################################

def test_create_all_accounts():
    """ Test creating multiple Accounts """
    for data in ACCOUNT_DATA:
        account = Account(**data)
        account.create()
    assert len(Account.all()) == len(ACCOUNT_DATA)

def test_create_an_account():
    """ Test Account creation using known data """
    rand = randrange(0, len(ACCOUNT_DATA))
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account(**data)
    account.create()
    assert len(Account.all()) == 1

def test_repr():
    """Test the representation of an account"""
    account = Account()
    account.name = "Foo"
    assert str(account) == "<Account 'Foo'>"

def test_to_dict():
    """Test account to dict"""
    rand = randrange(0, len(ACCOUNT_DATA))      # Generate a random index
    data = ACCOUNT_DATA[rand]       # Get a random account
    account = Account(**data)
    result = account.to_dict()

    assert account.name == result["name"]
    assert account.email == result["email"]
    assert account.phone_number == result["phone_number"]
    assert account.disabled == result["disabled"]
    assert account.date_joined == result["date_joined"]

def test_from_dict():
    rand = randrange(0, len(ACCOUNT_DATA))      # Generate a random index
    data = ACCOUNT_DATA[rand]       # Get a random account
    account = Account(**data)

    dict = {
        'name' : 'account_Name',
        'email': 'account_Email',
        'phone_number' : '7021234567',
        'disabled' : 'Maybe',
        'date_joined' : 'Today'
    }

    account.from_dict(dict)

    assert account.name == 'account_Name'
    assert account.email == 'account_Email'
    assert account.phone_number == '7021234567'
    assert account.disabled == 'Maybe'
    assert account.date_joined == 'Today'

def test_update():
    rand = randrange(0, len(ACCOUNT_DATA))      # Generate a random index
    data = ACCOUNT_DATA[rand]       # Get a random account
    account = Account(**data)

    # Test exception with empty id
    try:
        account.update()
    except DataValidationError as error:
        assert str(error) == "Update called with empty ID field"

    # Get a random id and do an update???
    account.id = 59498
    account.name = "new name"

    account.update()

def test_delete_and_find():
    rand = randrange(0, len(ACCOUNT_DATA))      # Generate a random index
    data = ACCOUNT_DATA[rand]       # Get a random account
    account = Account(**data)

    # Ensure that our found account is correct
    assert None == Account.find(12345678)

    # A valid account is found. Delete it and ensure it's deleted
    try:
        account.delete()
    except Exception as error:
        print("error: %s" % error)
