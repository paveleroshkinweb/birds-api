from flask import make_response


def version_controller():
    response = make_response('Birds Service. Version 0.1', 200)
    response.mimetype = 'text/plain'
    return response