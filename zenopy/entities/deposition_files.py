# -*- coding: utf-8 -*-

"""Zenodo _DepositionFiles class

"""

from xml.dom import ValidationErr
import requests
import validators
# import json
# from datetime import datetime, timezone
from entities.record import Record
from pathlib import Path
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
    
    def create_deposition_file(self, file_path: (str | Path) = None, bucket_url: str = None, record: Record = None) -> Record:
        """Upload a new file (into an existing deposition record)."""
        if file_path is not None and file_path != "":
            if isinstance(file_path, str):
                path = Path(file_path).expanduser()
            elif isinstance(file_path, Path):
                path = file_path.expanduser()
            else:
                raise TypeError(
                    "The 'file_path' should be of str or Path type."
                )
            if path.exists():
                if bucket_url is not None and isinstance(bucket_url, str):
                    tmp_url = bucket_url.strip().rstrip("/")
                elif record is not None and isinstance(record, Record):
                    tmp_url = record.data["links"]["bucket"]
                    print(tmp_url)
                else:
                    raise ValueError(
                        "Both 'bucket_url' and 'record' are of None or wrong type."
                    )
                is_valid = validators.url(tmp_url)
                is_valid = tmp_url.startswith(self._client._base_url + "/files")
                if is_valid:
                    with open(path, "rb") as fp:
                        response = requests.put(
                        url="%s/%s" % (tmp_url, path.name),
                        data=fp,
                        params=self._params,
                        )
                        status_code = response.status_code
                        if status_code not in [200, 201]:
                            zenodo_error(status_code)
                        return Record(self._client, record=response)
                else:
                    RuntimeError(
                        f"The provided path ({path}) is not valid."
                    )
        else:
            ValueError(
                "The 'file_path' argument cannot be None or empty."
            )

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