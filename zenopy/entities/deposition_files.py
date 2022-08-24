# -*- coding: utf-8 -*-

"""Zenodo _DepositionFiles class

"""

import requests
# import validators
# import json
# from datetime import datetime, timezone
from entities.record import Record
# from entities.metadata import ( 
#     upload_types, publication_types, image_types, creators_metadata,
#     access_rights,
#     )
from errors import zenodo_error, request_error
import logging

logger = logging.getLogger(__name__)

class _DepositionFiles(object):
    """The Deposition file resource is used for uploading 
    and editing files of a deposition on Zenodo."""
    def __init__(self, client):
        self._client = client
        self._params = client._params
        self._deposits_url = client._base_url + "/deposit/depositions/@id/files"
        self.data = {}
    
    def create_deposition_file(self):
        """Upload a new file (into an existing deposition record)."""
        tmp_url = self._deposits_url.strip().rstrip("/")

        response = requests.post(url=tmp_url, json={}, params=self._params)
        status_code = response.status_code
        if status_code != 201:
            zenodo_error(status_code)
        return Record(self._client, record=response)
    

    def retrieve_deposition_file(self, id_: int = None) -> Record:
        """Retrieve a single deposition file"""
        return Record(self._client, id_= id_, url = None, record = None)