# -*- coding: utf-8 -*-

"""HTTP status codes

"""

import requests
import json

status_code_dict = {
    200: {
        "name": "OK",
        "description": (
            "Request succeeded. Response included. Usually sent for "
            "GET/PUT/PATCH requests."
        ),
    },
    201: {
        "name": "Created",
        "description": (
            "Request succeeded. Response included. Usually sent for " "POST requests."
        ),
    },
    202: {
        "name": "Accepted",
        "description": (
            "Request succeeded. Response included. Usually sent for "
            "POST requests, where background processing is needed to fulfill the "
            "request."
        ),
    },
    204: {
        "name": "No Content",
        "description": (
            "Request succeeded. No response included. Usually sent "
            "for DELETE requests."
        ),
    },
    400: {
        "name": "Bad Request",
        "description": ("Request failed. Error response included."),
    },
    401: {
        "name": "Unauthorized",
        "description": (
            "Request failed, due to an invalid access token. "
            "Error response included."
        ),
    },
    403: {
        "name": "Forbidden",
        "description": (
            "Request failed, due to missing authorization (e.g. "
            "deleting an already submitted upload or missing scopes for your "
            "access token). Error response included."
        ),
    },
    404: {
        "name": "Not Found",
        "description": (
            "Request failed, due to the resource not being "
            "found. Error response included."
        ),
    },
    405: {
        "name": "Method Not Allowed",
        "description": (
            "Request failed, due to unsupported HTTP method. "
            "Error response included."
        ),
    },
    409: {
        "name": "Conflict",
        "description": (
            "Request failed, due to the current state of the "
            "resource (e.g. edit a deopsition which is not fully integrated). "
            "Error response included."
        ),
    },
    415: {
        "name": "Unsupported Media Type",
        "description": (
            "Request failed, due to missing or invalid request "
            "header Content-Type. Error response included."
        ),
    },
    429: {
        "name": "Too Many Requests",
        "description": (
            "Request failed, due to rate limiting. Error " "response included."
        ),
    },
    500: {
        "name": "Internal Server Error",
        "description": (
            "Request failed, due to an internal server error. "
            "Error response NOT included. Don't worry, Zenodo admins have been "
            "notified and will be dealing with the problem ASAP."
        ),
    },
}

def zenodo_error(status_code: int) -> None:
    if status_code is not None:
        if status_code in status_code_dict:
            name = status_code_dict[status_code]["name"]
            description = status_code_dict[status_code]["description"]
            raise RuntimeError(
                "The server request has resulted in an error with the following details:\n"
                f"Status: {name}\n"
                f"Status code: {status_code}\n"
                f"Description: {description}\n"
            )
        else:
            if status_code in requests.codes.__dict__.values():
                error_name = list(requests.codes.__dict__.keys())[
                    list(requests.codes.__dict__.values()).index(status_code)
                ]
                raise RuntimeError(
                    "The server request has resulted in an error with the following details: \n"
                    f"Status: {error_name}\n"
                    f"Status code: {status_code}\n"
                )
    else:
        raise ValueError("The status code cannot be None.")

def request_error(response: requests.models.Response = None) -> None:
    if response is not None:
        status_code = response.status_code
        if status_code not in [200, 201, 202, 204]:
            raise RuntimeError(
                "The server request has resulted in an error with the following details:\n"
                f"{json.dumps(response.json(), indent=4)}\n"
            )
    else:
        raise ValueError("The response argument cannot be None.")