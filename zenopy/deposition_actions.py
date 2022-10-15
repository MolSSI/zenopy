# -*- coding: utf-8 -*-

"""Zenodo _DepositionActions class

"""

import requests
import json
import logging

from zenopy.errors import request_error
from zenopy.metadata import deposition_actions
from zenopy.record import Record

logger = logging.getLogger(__name__)

class _DepositionActions(object):
    """The Deposition actions class for publishing, editing, discarding 
    and versioning of the Zenodo records/depositions."""
    def __init__(self, client):
        self._client = client
        self._params = client._params
        self._deposit_action_url = client._base_url + "/deposit/depositions/@id/actions"
        self.data = {}

    def deposition_action(self, id_: int = None, action: str = None, return_newversion: bool = True) -> "(None | Record)":
        """Performing actions on Zenodo depositions/records"""
        if id_ is not None and isinstance(id_, int):
            if action is not None and action != "":
                if action in deposition_actions.keys():
                    tmp_url = self._deposit_action_url.strip().replace("@id", str(id_))
                    tmp_url += f"/{action}"
                    response = requests.post(url=tmp_url, params=self._params)
                    status_code = response.status_code
                    if status_code not in [200, 201, 202]:
                        request_error(response=response)
                    else:
                        record = response.json()
                        if action == "newversion" and return_newversion:
                            if "latest_draft" in record["links"].keys():
                                return Record(self._client, url=record["links"]["latest_draft"])
                            else:
                                raise KeyError(
                                    "The 'latest_draft' key does not exist in the deposit/record."
                                )
                        else:
                            return Record(self._client, record=record)
                else:
                    raise ValueError(
                        "The 'action' argument can take one of the following values:\n"
                        f"{json.dumps(list(deposition_actions.keys()), indent=4)}"
                    )
            else:
                raise ValueError(
                    "The deposition file ID cannot be None or empty."
                )
        else:
            raise ValueError(
                "The deposition ID cannot be None and must be an integer."
            )
