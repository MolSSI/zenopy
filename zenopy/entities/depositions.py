# -*- coding: utf-8 -*-

"""Zenodo Depositions class

"""

import logging
from entity import Entity

logger = logging.getLogger(__name__)

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