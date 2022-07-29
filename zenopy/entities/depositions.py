# -*- coding: utf-8 -*-

"""Zenodo Depositions class

"""

import logging
import requests
import pprint
from datetime import datetime, timezone

import entities
from entities.entity import Entity
from entities import record
from errors import zenodo_error

logger = logging.getLogger(__name__)

deposition_form = {

}

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
        metadata: dict = None,
        modified: datetime = None,
        owner: int = None,
        record_url: str = None,
        state: str = 'unsubmitted',
        submitted: bool = False,
        title: str = None
    ):
        Entity.__init__(self)
        self._deposits_url = self._base_url + "/deposit/depositions"
        self.data = {}

        if created is None or created == "":
            self.data["created"] = datetime.now(timezone.utc).isoformat()
        self.data["doi"] = doi
        self.data["doi_url"] = doi_url
        self.data["files"] = files
        self.data["id"] = id_
        if metadata is None:
            self.data["metadata"] = {}
            self.data["metadata"]["title"] = title
        if modified is None or modified == "":
            self.data["modified"] = datetime.now(timezone.utc).isoformat()
        self.data["owner"] = owner
        self.data["record_url"] = record_url
        if state in ["unsubmitted", "inprogress", "done", "error"]:
            self.data["state"] = state
        else:
            raise ValueError(
                f"The given state ({state}) is not permitted.\n"
                "The valid states are 'unsubmitted', 'inprogress', 'done', or 'error'."
            )
        self.data["submitted"] = submitted
        self.data["title"] = title

    def create_deposition(self):
        """Create a new deposition/record object for uploading to Zenodo."""
        # r = requests.post(url=url, json={}, params=params)
        # r = requests.post(url=url, json={}, params=params, headers=headers)
        # r = requests.post(url=url, data="{}", params=params, headers=headers)
        response = requests.post(url=self._deposits_url, json={}, params=self._params)

        status_code = response.status_code
        if status_code != 201:
            zenodo_error(response.status_code)

        return record.Record(record=response)

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

    def update_deposition():
        """Update an existing deposition resource."""
        pass