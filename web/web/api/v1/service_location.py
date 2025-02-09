from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .response_wrapper import ApiResponseWrapper
from web.database import db
from web.models.service_location import ServiceLocation, ServiceLocationSchema

service_location_api_bp = Blueprint('service_location_api_bp', __name__)


@service_location_api_bp.route('/service_locations', methods=['GET'])
def get_service_location_ids():
    '''
    Retrieves all service location objects
    '''
    arw = ApiResponseWrapper()

    fields_to_filter_on = request.args.getlist('fields')

    if len(fields_to_filter_on) > 0:
        for field in fields_to_filter_on:
            if field not in ServiceLocation.__table__.columns:
                arw.add_errors({field: 'Invalid Service Location field'})
                return arw.to_json(None, 400)
    else:
        fields_to_filter_on = None

    service_locations = ServiceLocation.query.all()
    service_location_schema = ServiceLocationSchema(exclude=['address_id'],
                                                    only=fields_to_filter_on)
    results = service_location_schema.dump(service_locations, many=True)

    return arw.to_json(results)


@service_location_api_bp.route('/service_location/<int:service_location_id>',
                               methods=['GET'])
def show_service_location_info(service_location_id):
    '''
    Retrieves one service location object
    '''
    arw = ApiResponseWrapper()
    service_location_schema = ServiceLocationSchema(exclude=['address_id'])

    try:
        service_location = ServiceLocation.query.filter_by(
            service_location_id=service_location_id).one()

    except (MultipleResultsFound, NoResultFound):
        arw.add_errors('No result found or multiple results found')

    if arw.has_errors():
        return arw.to_json(None, 400)

    results = service_location_schema.dump(service_location)

    return arw.to_json(results)


@service_location_api_bp.route('service_location/<int:service_location_id>',
                               methods=['PUT'])
def modify_service_location(service_location_id):
    '''
    Updates one service location object in database
    '''
    arw = ApiResponseWrapper()
    service_location_schema = ServiceLocationSchema(
        exclude=['created_at', 'updated_at'])
    modified_service_location = request.get_json()

    try:
        ServiceLocation.query.filter_by(
            service_location_id=service_location_id).one()
        modified_service_location = service_location_schema.load(
            modified_service_location, session=db.session)
        db.session.commit()

    except (MultipleResultsFound, NoResultFound):
        arw.add_errors('No result found or multiple results found')

    except ValidationError as ve:
        arw.add_errors(ve.messages)

    except IntegrityError:
        arw.add_errors('Integrity error')

    if arw.has_errors():
        db.session.rollback()
        return arw.to_json(None, 400)

    results = service_location_schema.dump(modified_service_location)

    return arw.to_json(results)


@service_location_api_bp.route('/service_location', methods=['POST'])
def add_service_location():
    '''
    Adds new service location object to database
    '''
    arw = ApiResponseWrapper()
    service_location_schema = ServiceLocationSchema(
        exclude=['service_location_id', 'created_at', 'updated_at'])
    new_service_location = request.get_json()

    try:
        new_service_location = service_location_schema.load(
            new_service_location, session=db.session)
        db.session.add(new_service_location)
        db.session.commit()

    except ValidationError as ve:
        arw.add_errors(ve.messages)

    except IntegrityError:
        arw.add_errors('Integrity error')

    if arw.has_errors():
        db.session.rollback()
        return arw.to_json(None, 400)

    results = ServiceLocationSchema().dump(new_service_location)

    return arw.to_json(results)
