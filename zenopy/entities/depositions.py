# -*- coding: utf-8 -*-

"""Zenodo Depositions class

"""

import logging

logger = logging.getLogger(__name__)

import requests
import pprint
import validators
from datetime import datetime, timezone

import entities
from entities.record import Record
from errors import zenodo_error

from utils import disable_method

deposition_form = {}

class _Depositions(object):
    """Deposit provides API for uploading and editing published outputs
    on Zenodo as an alternative to the functionality provided by Zenodo's
    graphical user interface."""
    def __init__(self, client):
        self._client = client
        self._params = client._params
        self._deposits_url = client._base_url + "/deposit/depositions/"
        self.data = {}

    def create_config_file(self, config_file_path: str = None) -> None:
        disable_method(
            "The 'create_config_file()' must be called from Zenodo superclass."
        )

    def create_deposition(self):
        """Create a new deposition/record object for uploading to Zenodo."""
        # r = requests.post(url=url, json={}, params=params)
        # r = requests.post(url=url, json={}, params=params, headers=headers)
        # r = requests.post(url=url, data="{}", params=params, headers=headers)
        tmp_url = self._deposits_url.strip().rstrip("/")
        response = requests.post(url=tmp_url, json={}, params=self._params)
        status_code = response.status_code
        if status_code != 201:
            zenodo_error(status_code)
        return Record(self._client, record=response)

    def delete_deposition(self, id_: int = None, url: str = None) -> None:
        """Delete an existing deposition resource.
        Note: only unpublished depositions may be deleted."""
        if id_ is not None and isinstance(id_, int):
            # TODO: Take care of the url parsing with urllib.parse module
            tmp_url = self._deposits_url + str(id_)
            response = requests.delete(url=tmp_url, params=self._params)
        elif url is not None:
            url = url.strip().rstrip("/")
            is_valid = validators.url(url)
            is_valid = url.startswith(self._deposits_url)
            if is_valid:
                response = requests.delete(url=url, params=self._params)
            else:
                raise ValueError(
                    f"The provided URL ({url}) is invalid.\n"
                    "Please enter a valid URL."
                )
        else:
            raise RuntimeError("Please provide a valid record URL, ID or object.")
        status_code = response.status_code
        if status_code in [201, 204]:
            logger.warning(
                "An unpublished deposition has been deleted at the following address:\n"
                f"\t{self._deposits_url}\n"
            )
        else:
            zenodo_error(status_code)
        # elif record is not None or record == {}:
        #     if isinstance(record, Record):
        #         idd = record._id
        #     elif isinstance(record, requests.models.Response):
        #         response = record.json()
        #         idd = response["id"]
        #     elif isinstance(record, dict):
        #         idd = record["id"]
        #     else:
        #         raise TypeError(
        #             f"The provided record type ({type(record)}) is invalid.\n"
        #             "Record type should be either \n"
        #             "(entities.Record | requests.models.Response | dict)."
        #         )
        #     if isinstance(record, list):
        #         raise RuntimeError(
        #             "The provided data is a list of records. "
        #             "A single record must be provided."
        #         )
        #     tmp_url = self._deposits_url + str(idd)
        #     response = requests.delete(url=tmp_url, params=self._params)
        # else:
        #     raise RuntimeError("Please provide a valid record URL, ID or object.")

    def list_depositions(
        self,
        query: (str | dict) = None,
        status: str = "draft",
        sort: str = "bestmatch",
        page: int = 1,
        size: int = 25,
        all_versions: (int | bool) = False,
    ) -> list:
        """List all depositions available to the current user identified
        by the active authentication and match the query statement."""
        tmp_params = self._params.copy()
        if query is not None or query != "":
            tmp_params["q"] = query
        else:
            query = ""
        if status is not None:
            if status in ["draft", "published"]:
                tmp_params["status"] = status
            else:
                raise ValueError(
                    f"Invalid status argument value ({status}).\n"
                    "The status argument can either be 'draft' or 'published.\n"
                )
        else:
            logger.warning(
                "The value of status argument is None.\n"
                "ZenoPy will only list the published records."
            )
            status = "published"
            tmp_params["status"] = status
        if sort is not None:
            if sort in ["bestmatch", "mostrecent", "-mostrecent"]:
                tmp_params["status"] = status
            else:
                raise ValueError(
                    f"Invalid sort argument value ({sort}).\n"
                    "The sort argument can either be 'bestmatch', "
                    "'mostrecent' (ascending), '-mostrecent' (descending)."
                )
        else:
            logger.warning(
                "The value of sort argument is None.\n"
                "ZenoPy will prioritize the best matching records."
            )
            sort = "bestmatch"
            tmp_params["sort"] = sort
        if page is not None and isinstance(page, int):
            tmp_params["page"] = page
        else:
            logger.warning(
                "ZenoPy will use pagination of 25 for this search "
                "because the 'page' argument used is either None or not an integer."
            )
            page = 25
            tmp_params["page"] = page
        if size is not None and isinstance(size, int):
            tmp_params["size"] = size
        else:
            raise TypeError(
                "ZenoPy will return 1 search result in this case "
                "because the 'size' argument used is either None or not an integer."
            )
        if all_versions is not None and all_versions in [0, 1, False, True]:
            tmp_params["all_versions"] = all_versions
        else:
            logger.warning(
                "ZenoPy will return the latest version for this search "
                "because the 'all_version' argument used is either None or "
                "not a binary integer or boolean."
            )
        tmp_url = self._deposits_url.strip().rstrip("/")
        response = requests.get(url=tmp_url, params=tmp_params)
        search_result = response.json()
        records_list = []
        if isinstance(search_result, list):
            for record in search_result:
                records_list.append(Record(self._client, record=record))
            return records_list
        else:
            return search_result

    def retrieve_deposition(self, id_: int = None) -> Record:
        """Retrieve a single deposition resource."""
        return Record(self._client, id_= id_, url = None, record = None)

    def update_deposition(
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
        state: str = "unsubmitted",
        submitted: bool = False,
        title: str = None,
    ) -> None:
        """Update an existing deposition resource."""
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
