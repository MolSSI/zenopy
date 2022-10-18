# -*- coding: utf-8 -*-

"""Zenodo Utility Modules

"""


@staticmethod
def disable_method(msg: str = None):
    if msg is not None and msg != "":
        if isinstance(msg, str):
            raise AttributeError(msg)
        else:
            raise TypeError("The message argument should be of string type.")
    else:
        raise RuntimeError(
            "The error message in the 'disable_method()' cannot be empty or None."
        )
