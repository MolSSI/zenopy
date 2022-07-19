# -*- coding: utf-8 -*-

"""Zenodo Entities

"""

from argparse import ArgumentError
import collections.abc
import requests
import validators
import logging
import pprint
from datetime import datetime, timezone

from client import Zenodo
# import metadata

logger = logging.getLogger(__name__)

class Entity(Zenodo):
    def __init__(self):
        Zenodo.__init__(self)
        self._data = {}
        self._metadata = {}
        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self._params = {}
        self._params["access_token"] = self.token

class Communities(Entity):
    """Communities class offers APIs for searching 
    the Zenodo communities."""
    pass

class Depositions(Entity):
    """Deposit provides API for uploading and editing published outputs
    on Zenodo as an alternative to the functionality provided by Zenodo's 
    graphical user interface."""
    def __init__(
        self,
        created: datetime = None,
        doi: str = None,
        doi_url: str = None,
        files: list = None,
        id_: int = None,
        metadata: object = None,
        modified: datetime = None,
        owner: int = None,
        record_url: str = None,
        state: str = 'inprogress',
        submitted: bool = False,
        title: str = None
    ):
        Entity.__init__(self)
        self._base_deposit_url = self._base_url + "/deposit/depositions"
        self._response = None

        if created is None or created == "":
            self._created = datetime.now(timezone.utc).isoformat()
        self.doi = doi
        self.doi_url = doi_url
        self.files = files
        self.id = id_
        # if metadata is None:

        if modified is None or modified == "":
            self._modified = datetime.now(timezone.utc).isoformat()
        self.owner = owner
        self.record_url = record_url
        if state in ["inprogress", "done", "error"]:
            self.state = state
        else:
            raise ValueError(
                f"The given state ({state}) is not permitted.\n"
                "The valid states are 'inprogress', 'done', 'error'."
            )
        self.submitted = submitted
        self.title = title

    def list_depositions(
        self,
        query: str = None,
        status: str = "draft",
        sort: str = "bestmatch",
        page: int = 1,
        size: int = 25,
        all_versions: (int | bool) = False 
    ) -> list:
        """List all depositions available to the current user identified 
        by the active authentication and match the query statement."""
        payload = self._params.copy()
        if query is not None or query != "":
            tmp_params["q"] = query
        else:
            query = ""
            
        response = requests.get(self._base_deposit_url, params = tmp_params)
        return response.json()

class DepositionFiles(Entity):
    """The Deposition file resource is used for uploading 
    and editing files of a deposition on Zenodo."""
    pass

class Funders(Entity):
    """Funders class offers APIs for searching research funders on 
    Zenodo servers."""
    pass

class Grants(Entity):
    """Grants class implements APIs for searching the Zenodo Grants"""
    pass

class Licenses(Entity):
    """Licenses class provides APIs for searching licenses on Zenodo servers."""
    pass

class Record(collections.abc.MutableMapping, Entity):
    """Zenodo Record mixin container class"""
    def __init__(self, id_: int = None, url: str = None, record: requests.models.Response = None):
        Entity.__init__(self)
        if id_ is not None and isinstance(id_, int):
            self.record_url = self._base_url + "/records/" + str(id_)
            response = requests.get(self.record_url, params=self._params, headers=self._headers)
            self.data = response.json() 
        elif url is not None:
            url = url.strip().rstrip("/")
            is_valid = validators.url(url)
            if is_valid:
                self.record_url = url
                response = requests.get(self.record_url, params=self._params, headers=self._headers)
                self.data = response.json()
            else:
                raise ValueError(
                    f"The provided URL ({url}) is invalid.\n"
                    "Please enter a valid URL."
                )
        elif record is not None or record == {}:
            if isinstance(record, Record):
                self.data = record.data
            elif isinstance(record, requests.models.Response):
                self.data = record.json()
            elif isinstance(record, dict):
                self.data = record
            else:
                raise TypeError(
                    f"The provided record type ({type(record)}) is invalid.\n"
                    "Record type should be either \n"
                    "(entities.Record | requests.models.Response | dict)."
                )
            if isinstance(self.data, list):
                raise RuntimeError(
                    "The provided data is a list of records. "
                    "A single record must be provided."
                )
            key = "links" if "links" in self.data else "latest"
            self.record_url = self.data[key]["self"]
        else:
            raise RuntimeError(
                "Please provide a valid record URL, ID or object."

            )

    # Provide dict like access to the Record container (dictionary data)
    def __getitem__(self, key: (int | slice)) -> dict:
        """Allow access to data via indexing/slicing"""
        return self.data[key]

    def __setitem__(self, key: (int | slice), value) -> None:
        """Manage assignments through indexing/slicing"""
        self.data[key] = value

    def __delitem__(self, key: (int | slice)) -> None:
        """Deleting entri(es) from record data through indexing/slicing"""
        del self.data[key]

    def __iter__(self):
        """Allow iteration over the object"""
        return iter(self.data)

    def __len__(self):
        """The len() command"""
        return len(self.data)

    def __str__(self):
        return pprint.pformat(self.data)

    @property
    def created(self) -> str:
        """Creation time of deposition (in ISO8601 format)."""
        if "created" in self.data and self.data["created"] != "":
            return self.data["created"]
        else:
            raise RuntimeError(
                "The creation time of the record is not set."
            )

    @created.setter
    def created(self, created: str = None):
        """Setting the time of creation for the deposition/record."""
        if created is not None and created != "":
            if "created" in self.data and self.data["created"] != "":
                logger.warning(
                    "You are attempting to replace the creation time of the record."
                )
            self.data["created"] = created
        else:
            raise ValueError(
                "The creation time for the record cannot be empty or None."
            )

    @property
    def doi(self) -> str:
        """Digital Object Identifier (DOI). When you publish your 
        deposition, Zenodo registers a DOI in DataCite for your upload, 
        unless you manually provided Zenodo with one. This field is only
        present for published depositions."""
        if "doi" in self.data and self.data["doi"] != "":
            return self.data["doi"]
        elif "doi" in self.data["metadata"] and self.data["metadata"]["doi"] != "":
            return self.data["metadata"]["doi"]
        else:
            return self.data["metadata"]["prereserve_doi"]["doi"]
    
    @doi.setter
    def doi(self, doi: str = None) -> None:
        """Setting the Digital Object Identifier (DOI) in the 
        record object."""
        if doi is not None and doi != "":
            self.data["doi"] = str(doi)
            self.data["metadata"]["doi"] = str(doi)
            self.data["metadata"]["prereserve_doi"]["doi"] = str(doi)
        else:
            raise ValueError(
                "The DOI for the record cannot be empty or None."
            )

    @property
    def doi_url(self):
        """Persistent link to your published deposition. 
        This field is only present for published depositions."""
        if "doi_url" in self.data:
            return self.data["doi_url"]
        elif "links" in self.data and self.data["links"]["doi"] != "":
            return self.data["links"]["doi"]
        else:
            return "https://doi.org/" + str(self.doi)
    
    @doi_url.setter
    def doi_url(self, doi_url: str = None):
        """Setting the Digital Object Identifier (DOI) URL in the 
        record object."""
        if doi_url is not None and doi_url != "":
            self.data["doi_url"] = str(doi_url)
            self.data["links"]["doi"] = str(doi_url)
        else:
            raise ValueError(
                "The DOI URL for the record cannot be empty or None."
            )

    @property
    def files(self) -> list:
        """A list of deposition files resources."""
        if "files" in self.data and self.data["files"] != []:
            return self.data["files"]
    
    @property
    def _id(self) -> int:
        """Deposition identifier."""
        if "id" in self.data and self.data["id"] != "":
            return self.data["id"]
        elif "record_id" in self.data and self.data["record_id"] != "":
            return self.data["record_id"]
        else:
            raise RuntimeError(
                "The (record-)id is not set or accessible."
            )
    
    @_id.setter
    def _id(self, idx: int = None) -> None:
        if idx is not None and isinstance(idx, int):
            self.data["id"] = int(idx)
            self.data["record_id"] = int(idx)
        else:
            raise TypeError(
                f"The record ID ({type(idx)}) is of invalid type."
            )
    
    @property
    def metadata(self) -> dict:
        """A deposition metadata resource."""
        if "metadata" in self.data and self.data["metadata"] != {}:
            return self.data["metadata"]
        else:
            raise RuntimeError(
                "The record metadata is not set or accessible."
            )


class Records(Entity):
    """Records class offers search capabilities for published records 
    on Zenodo."""
    def __init__(self, response: requests.models.Response = None):
        Entity.__init__(self)
        self._base_records_url = self._base_url + "/deposit/depositions"
        if response is not None:
            self._response = response.json()

    def add_version(self, _id):
        """Create a new record object for uploading a new version to Zenodo."""
        url = self.base_url + f"/deposit/depositions/{_id}/actions/newversion"
        response = requests.post(url, headers=headers)

        if response.status_code != 201:
            raise RuntimeError(
                f"Error in add_version: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        # The result is for the original DOI, so get the data for the new one
        url = result["links"]["latest_draft"]
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in add_version get latest draft: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, self.token)

    def create_record(self):
        """Create a new record object for uploading to Zenodo."""
        response = requests.post(self._base_records_url, headers=self._headers)

        if response.status_code != 201:
            raise RuntimeError(
                f"Error in create_record(): code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, self.token)

    def get_deposit_record(self, _id):
        """Get an existing deposit record object from Zenodo."""
        url = self.base_url + f"/deposit/depositions/{_id}"
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        except Exception:
            token = None
            response = requests.get(url, json={})
        else:
            token = self.token
            response = requests.get(url, json={}, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in get_deposit_record: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, token)

    def get_record(self, _id):
        """Get an existing record object from Zenodo."""
        url = self.base_url + f"/api/records/{_id}"
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        except Exception:
            response = requests.get(url, json={})
        else:
            response = requests.get(url, json={}, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in get_record: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, None)

    def search(
        self,
        authors=None,
        query="",
        communities=None,
        keywords=None,
        title=None,
        description=None,
        all_versions=False,
        size=25,
        page=1,
    ):
        """Search for records in Zenodo."""
        url = self.base_url + "/records/"

        payload = {
            "size": size,
            "page": page,
        }
        if all_versions:
            payload["all_versions"] = 1

        if communities is not None:
            for community in communities:
                query += f' AND +communities:"{community}"'

        if keywords is not None:
            for keyword in keywords:
                query += f' AND +keywords:"{keyword}"'

        payload["q"] = query

        logger.debug("Payload for query request:\n" + pprint.pformat(payload))

        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
            }
        except Exception:
            response = requests.get(url, params=payload)
        else:
            response = requests.get(url, headers=headers, params=payload)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in search: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        records = []
        if "hits" in result:
            hits = result["hits"]
            n_hits = hits["total"]

            logger.debug(f"{n_hits=}")

            for record in hits["hits"]:
                records.append(Record(record, None))

            for record in records:
                logger.debug(f"\t{record['id']}: {record['metadata']['title']}")
        else:
            logger.debug("Query returned no hits!")

        return n_hits, records
