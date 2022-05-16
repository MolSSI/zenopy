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