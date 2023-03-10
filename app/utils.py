import flask_restx
from app.models import User, Entity, Advice
import datetime as dt
import requests

def create_from_entity(type, **kwargs) -> object:
    '''
    Creates an Entity dependent object. These objects are not committed so they have to be saved manually.

    :param type: type of object to create from entity
    :type type: str
    :kwargs: any parameters needed to create the object
    :kwargs: dict
    :return: Object of selected by type. Example: if "advice" the and Advice object is returned.
    :rtype: Entity, object
    '''
    
    assert isinstance(type, str)
    type = type.lower()

    entity = Entity(type = type)
    
    if type == 'advice':
        object = Advice(entity=entity, **kwargs)
    else:
        #TODO add all possible types
        pass
    
    return entity, object



def get_adviceslip_by_id(adviceslip_id) -> tuple:

    '''
    Wrapper for Advice Slip's 'Advice by Id' endpoint.
    If an advice slip is found with the corresponding {slip_id}, a slip object is returned.
    A slip object is returned by the endpoint if an advice slip is found with the corresponding {slip_id}:
    
        {
            "slip": {
                "slip_id": "2",
                "advice": "Smile and the world smiles with you. Frown and you're on your own."
            }
        }

    If the slip is not found or if there is an error, a message object is returned:
        {
        "message": {
            "type": "notice",
            "text": "Advice slip not found."
            }
        }

    :param id: The id of the advice slip.
    :type id: int
    :return: request outcome, content 
    :rtype: bool, string
    '''

    url = f'https://api.adviceslip.com/advice/{adviceslip_id}'

    response = requests.get(url)

    if "slip" in response.json():
        return True, response.json()['slip']['advice']
    else:
        return False, response.json()['text']


def user_attr_unique_notempty_check(attributes_to_check, user_to_update=None) -> tuple:
    """
    description

    :param attributes_to_check: dictionary of attributes to in User Object
    :type attributes_to_check: dict
    :param user: required for update check otherwise function will always return False.
    :type user: User
    :return: tuple with status, status code and a message. If there is an error, the tuple will be (False, msg)
    :rtype: tuple
    """

    status = True
    status_code = 200
    msg = []

    if user_to_update:
        username_to_update = user_to_update.username
        email_to_update = user_to_update.email
    else:
        username_to_update = None
        email_to_update = None

    empty_checks = [None, ""]

    if "username" in attributes_to_check.keys():
        new_username = attributes_to_check["username"]
        if new_username in empty_checks:
            msg.append("ERROR: Username attribute provided but is empty")
            status = False
            status_code = 409
        elif User.query.filter(
            User.username == new_username, User.username != username_to_update
        ).first():
            msg.append("CONFLICT: Username already exists")
            status = False
            status_code = 409
        else:
            msg.append("Username is valid for update/create")
    else:
        pass

    if "password" in attributes_to_check.keys():
        new_password = attributes_to_check["password"]
        if new_password in empty_checks:
            msg.append("ERROR: Password attribute provided but is empty")
            status = False
            status_code = 409
        else:
            msg.append("Password is valid for update/create")

    if "email" in attributes_to_check.keys():
        new_email = attributes_to_check["email"]
        if new_email in empty_checks:
            msg.append("ERROR: Email attribute provided but is empty")
            status = False
            status_code = 409
        elif User.query.filter(
            User.email == new_email, User.email != email_to_update
        ).first():
            msg.append("CONFLICT: Email already exists")
            status = False
            status_code = 409
        else:
            msg.append("Email is valid for update/create")
    else:
        pass

    # If all checks pass, return success
    return status, status_code, msg


def commit_to_db(db) -> tuple:
    """
    description

    :param db: database in current app context
    :type db: flask_sqlalchemy.SQLAlchemy
    :return: tuple with bool and a message. If there is an error, the tuple will be (False, Exception)
    :rtype: tuple
    """

    try:
        db.session.commit()
        return True, "success"

    except Exception as e:
        print(str(e))
        db.session.rollback()
        return False, e


def create_flaskrestx_parser(
    model, location="form"
) -> flask_restx.reqparse.RequestParser:
    """
    Creates a flask_restx.reqparse.RequestParser object from a flask_restx.Api.model

    :param model: Model to create parser from
    :type model: flask_restx.Api.model
    :param location: Location parameter for flask_restx.reqparse.RequestParser.add_argument(). Example: headers, form
    type location: str
    :return: Request parser object
    :rtype: flask_restx.reqparse.RequestParser:
    """

    parser = flask_restx.reqparse.RequestParser()
    for param, param_type in model.items():
        if isinstance(param_type, str):
            parser.add_argument(param, type=str, location=location)
        if isinstance(param_type, float):
            parser.add_argument(param, type=float, location=location)
        if isinstance(param_type, int):
            parser.add_argument(param, type=int, location=location)
        if isinstance(param_type, bool):
            parser.add_argument(param, type=bool, location=location)
        if isinstance(param_type, list):
            parser.add_argument(param, type=list, location=location)
        else:
            parser.add_argument(param)

    return parser


def validate_date_format(str_date) -> bool:
    """
    Checks if a str date is in the correct format.
    Expects format as yyyy-mm-dd == %Y-%m-%d

    :param date: date as string
    :type date: str
    :return: True if valid, False otherwise
    :rtype: bool
    """

    try:
        if str_date != dt.datetime.strptime(str_date, "%Y-%m-%d").strftime("%Y-%m-%d"):
            raise ValueError
        return True
    except ValueError:
        return False
