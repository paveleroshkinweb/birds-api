from contextlib import closing
from psycopg2.extras import DictCursor
import psycopg2
from flask import make_response, jsonify


db_config = {
    'dbname': 'birds_db',
    'user': 'ornithologist',
    'password': 'ornithologist',
    'host': 'localhost'
}


def birds_controller(args):
    invalid_param, hint = find_invalid_param(args)
    if invalid_param:
        invalid_params_response = make_response(
            f'Invalid {invalid_param} value {args.get(invalid_param)}. {hint}', 
            422
        )
        invalid_params_response.mimetype = 'text/plain'
        return invalid_params_response
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(form_query(args))
            birds = [map_bird_to_dict(bird) for bird in cursor.fetchall()]
            return jsonify(birds)


def form_query(args):
    params = {}
    query = 'SELECT * FROM birds {attribute} {offset} {limit};'
    statements = {
        'attribute': f'ORDER BY {args.get("attribute")} {args.get("order", "")}',
        'offset': f'OFFSET {args.get("offset")}',
        'limit': f'LIMIT {args.get("limit")}'        
    }
    for key, value in statements.items():
        params[key] = value if args.get(key) else ''
    return query.format(**params)            


def find_invalid_param(args):

    def is_valid_int(offset):
        try:
            offset = int(offset or 1)
            return offset > 0
        except ValueError:
            return False

    whitelists = {
        'attribute': ['', 'species', 'name', 'color', 'body_length', 'wingspan'],
        'order': ['', 'asc', 'desc']
    }
    hints = {
        'attribute': f'Please use value from: {" ".join(whitelists["attribute"]).strip()}',
        'order': f'Please use value from: {" ".join(whitelists["order"]).strip()}',
        'offset': f'Offset value should be positive integer',
        'limit': f'Limit value should be positive integer'
    }
    validators = {
        'attribute': lambda attr: attr in whitelists['attribute'],
        'order': lambda order: order in whitelists['order'],
        'offset': is_valid_int,
        'limit': is_valid_int
    }
    for prop, validator in validators.items():
        if not validator(args.get(prop, '')):
            return prop, hints[prop]
    return None, None


def map_bird_to_dict(values):
    fields = ['species', 'name', 'color', 'body_length', 'wingspan']
    return {key: value for key, value in zip(fields, values)}