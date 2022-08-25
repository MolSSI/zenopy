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
    
    def create_deposition_file(self) -> Record:
        """Upload a new file (into an existing deposition record)."""
        response = requests.post(url=tmp_url, json={}, params=self._params)
        status_code = response.status_code
        if status_code not in [200, 201]:
            zenodo_error(status_code)
        return Record(self._client, record=response)

    def list_deposition_files(self, id_: int = None) -> list[Record]:
        """List all deposition files for a given deposition"""
        if id_ is not None and isinstance (id_, int):
            tmp_url = self._deposits_url.strip().replace("@id", str(id_))
        else:
            raise ValueError(
                "The deposition ID cannot be None and must be an integer."
            )
        response = requests.get(url=tmp_url, params=self._params)
        status_code = response.status_code
        if status_code not in [200, 201]:
            zenodo_error(status_code)
        search_result = response.json()
        records_list = []
        if isinstance(search_result, list):
            for record in search_result:
                records_list.append(Record(self._client, record=record))
            return records_list
        else:
            return search_result

    def retrieve_deposition_file(self, id_: int = None, file_id: str =  None) -> Record:
        """Retrieve a single deposition file"""
        if id_ is not None and isinstance (id_, int):
            if file_id is not None and file_id != "":
                tmp_url = self._deposits_url.strip().replace("@id", str(id_))
                tmp_url += f"/{file_id}"
            else:
                raise ValueError(
                    "The deposition file ID cannot be None or empty."
                )
        else:
            raise ValueError(
                "The deposition ID cannot be None and must be an integer."
            )
        return Record(self._client, id_= None, url = tmp_url, record = None)