# -*- coding: utf-8 -*-

"""Zenodo Entities

"""

import collections.abc
import requests
import logging
from datetime import datetime, timezone

from client import Zenodo
import metadata

logger = logging.getLogger(__name__)

class Entity(Zenodo):
    def __init__(self):
        Zenodo.__init__(self)
        self._data = {}
        self._metadata = {}
        self._headers = {
            "Authorization": f"Bearer {self._token}",
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
    ) -> Deposit:
        Entity.__init__(self)
        self._base_deposit_url = self._base_url + "/deposit/depositions"
        self._response = None

        if created is None or created == "":
            self._created = datetime.now(timezone.utc).isoformat()
        self.doi = doi
        self.doi_url = doi_url
        self.files = files
        self.id = id_
        if metadata is None:

        if modified is None or modified == "":
            self._modified = datetime.now(timezone.utc).isoformat()
        self.owner = owner
        self.record_url = record_url
        if state is in ["inprogress", "done", "error"]
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

class Files(Entity):
    """Files provides APIs for (up|down)-loading the files."""
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
    def __init__(self, data: requests.models.Response = None):
        Entity.__init__(self)
        self.data = data
        if self.data in None or self.data == {}:
            logger.warning(
                "WARNING: The initialized Record object is empty."
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
