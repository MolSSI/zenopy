# -*- coding: utf-8 -*-

"""HTTP Status Codes

"""

status_code = {
    200: {
    "name":"OK",
    "description": ("Request succeeded. Response included. Usually sent for "
    "GET/PUT/PATCH requests.")
    },
    201: {
    "name": "Created",
    "description": ("Request succeeded. Response included. Usually sent for "
    "POST requests.")
    },
    202: {
    "name": "Accepted",
    "description": ("Request succeeded. Response included. Usually sent for "
    "POST requests, where background processing is needed to fulfill the "
    "request.")
    },
    204: {
    "name": "No Content",
    "description": ("Request succeeded. No response included. Usually sent "
    "for DELETE requests.")
    },
    400: {
    "name": "Bad Request",
    "description": ("Request failed. Error response included.")
    },
    401: {
    "name": "Unauthorized",
    "description": ("Request failed, due to an invalid access token. "
    "Error response included.")
    },
    403: {
    "name": "Forbidden",
    "description": ("Request failed, due to missing authorization (e.g. "
    "deleting an already submitted upload or missing scopes for your "
    "access token). Error response included.")
    },
    404: {
    "name": "Not Found",
    "description": ("Request failed, due to the resource not being "
    "found. Error response included.")
    },
    405: {
    "name": "Method Not Allowed",
    "description": ("Request failed, due to unsupported HTTP method. "
    "Error response included.")
    },
    409: {
    "name": "Conflict",
    "description": ("Request failed, due to the current state of the "
    "resource (e.g. edit a deopsition which is not fully integrated). "
    "Error response included.")
    },
    415: {
    "name": "Unsupported Media Type",
    "description": ("Request failed, due to missing or invalid request "
    "header Content-Type. Error response included.")
    },
    429: {
    "name": "Too Many Requests",
    "description": ("Request failed, due to rate limiting. Error "
    "response included.")
    },
    500: {
    "name": "Internal Server Error",
    "description": ("Request failed, due to an internal server error. "
    "Error response NOT included. Don't worry, Zenodo admins have been "
    "notified and will be dealing with the problem ASAP.")
    },
}

class Error(object):
    """A class for handling Zenodo error responses
    
    Attributes
    ----------
    response : dict
        Error responses for 400 series errors (e.g. 400, 401, 403, ...)
        are returned as a JSON object with two attributes 'message' and
        'status' (HTTP status code), and possibly an attribute 'errors' 
        with a list of more detailed errors.
        See https://developers.zenodo.org/#errors
    status : int
        The HTTP status codes to indicate success or failure of a request.
        See https://developers.zenodo.org/#http-status-codes
    message : str
        A human-readable explanation of the error.
    errors : dict
        The attribute 'errors', a JSON array of objects, each with the attributes
        'message' (with a human-readable explanation of the error), and possibly 
        'field' (with the “path” to field that contains the error).
    """

    def __init__(self, response: dict):
        self._response = response

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value