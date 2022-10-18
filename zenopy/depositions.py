# -*- coding: utf-8 -*-

"""Zenodo _Depositions class

"""

import requests
import validators
import json
from typing import Any
from datetime import datetime, timezone
import logging
from zenopy.metadata import (
    upload_types,
    publication_types,
    image_types,
    creators_metadata,
    access_rights,
)
from zenopy.record import Record
from zenopy.errors import zenodo_error, request_error

logger = logging.getLogger(__name__)


class _Depositions(object):
    """Deposit provides API for uploading and editing published outputs
    on Zenodo as an alternative to the functionality provided by Zenodo's
    graphical user interface."""

    def __init__(self, client):
        self._client = client
        self._params = client._params
        self._deposits_url = client._base_url + "/deposit/depositions/"
        self.data = {}

    def create_deposition(self):
        """Create a new deposition/record object for uploading to Zenodo."""
        # TODO: allow metadata to be passed for initialization instead of
        # only an empty deposition
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
            raise RuntimeError("Please provide a valid record URL or ID.")
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
        query: Any = None,
        status: str = "published",
        sort: str = "bestmatch",
        page: int = 1,
        size: int = 20,
        all_versions: (int | bool) = False,
    ) -> list[Record]:
        """List all depositions available to the current user identified
        by the active authentication and match the query statement."""
        tmp_params = self._params.copy()
        # For how to search, see https://help.zenodo.org/guides/search/
        if query is not None and query != "":
            tmp_params["q"] = query
        else:
            query = ""
        if status is not None:
            if status in ["draft", "published"]:
                tmp_params["status"] = status
            else:
                raise ValueError(
                    f"Invalid status argument value ({status}).\n"
                    "The status argument can either be 'draft' or 'published'."
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
                tmp_params["sort"] = sort
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
                "ZenoPy will use pagination of 20 for this search "
                "because the 'page' argument used is either None or not an integer."
            )
            tmp_params["page"] = 20
        if size is not None and isinstance(size, int):
            tmp_params["size"] = size
        else:
            raise TypeError(
                "ZenoPy will return 1 search result in this case "
                "because the 'size' argument used is either None or not an integer."
            )
        if all_versions in [0, 1, False, True]:
            tmp_params["all_versions"] = all_versions
        else:
            logger.warning(
                "ZenoPy will return the latest version for this search "
                "because the 'all_version' argument used is either None or "
                "non-(binary | boolean)."
            )
            tmp_params["all_versions"] = False
        tmp_url = self._deposits_url.strip().rstrip("/")
        response = requests.get(url=tmp_url, params=tmp_params)
        status_code = response.status_code
        if status_code != 200:
            zenodo_error(status_code)
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
        if id_ is not None and isinstance(id_, int):
            return Record(self._client, id_=id_, url=None, record=None)
        else:
            raise ValueError("The deposition ID cannot be None and must be an integer.")

    def update_deposition(
        self,
        id_: int = None,
        url: str = None,
        upload_type: str = None,
        publication_type: str = None,
        image_type: str = None,
        publication_date: str = None,
        title: str = None,
        creators: list[dict] = None,
        description: str = None,
        access_right: str = None,
        license: str = None,
        embargo_date: str = None,
        access_conditions: str = None,
    ) -> Record:
        """Update an existing deposition resource (deposition metadata)"""
        tmp_params = self._params.copy()
        tmp_metadata = {}
        if id_ is not None and isinstance(id_, int):
            deposit = self.retrieve_deposition(id_=id_)
            if url is None or url == "":
                tmp_url = deposit.record_url
        elif url is not None:
            url = url.strip().rstrip("/")
            is_valid = validators.url(url)
            is_valid = url.startswith(self._deposits_url)
            if is_valid:
                tmp_url = url
                # Check to see if a given URL does actually exist
                deposit = Record(self._client, url=tmp_url)
            else:
                raise ValueError(
                    f"The provided URL ({url}) is invalid.\n"
                    "Please enter a valid URL."
                )
        else:
            raise ValueError("Please provide a valid record URL or ID.")
        # Retrieve the existing metadata to update
        data = deposit.data
        if any(data["metadata"]):
            tmp_metadata = data["metadata"].copy()

        if upload_type is not None and upload_type != "":
            if upload_type not in upload_types.keys():
                raise ValueError(
                    "The 'upload_type' argument can take one of the following values:\n"
                    f"{json.dumps(list(upload_types.keys()), indent=4)}"
                )
            else:
                tmp_metadata["upload_type"] = upload_type
        else:
            raise ValueError("The 'upload_type' argument cannot be None or empty.")

        if upload_type == "publication":
            if publication_type is not None and publication_type != "":
                if publication_type in publication_types.keys():
                    tmp_metadata["publication_type"] = publication_type
                else:
                    raise ValueError(
                        "The 'publication_type' value can take one of the following values:\n"
                        f"{json.dumps(list(publication_types.keys()), indent=4)}"
                    )
            else:
                raise ValueError(
                    "The 'publication_type' argument cannot be None or empty."
                )
        elif upload_type == "image":
            if image_type is not None and image_type != "":
                if image_type in image_types.keys():
                    tmp_metadata["image_type"] = image_type
                else:
                    raise ValueError(
                        "The 'image_type' value can take one of the following values:\n"
                        f"{json.dumps(list(image_types.keys()), indent=4)}"
                    )
            else:
                raise ValueError("The 'image_type' argument cannot be None or empty.")

        if publication_date is not None and publication_date != "":
            tmp_metadata["publication_date"] = publication_date
        else:
            tmp_metadata["publication_date"] = datetime.now(timezone.utc).isoformat()

        if title is not None and title != "":
            tmp_metadata["title"] = title
        else:
            raise ValueError("The 'title' argument cannot be None or empty.")

        if creators is not None and isinstance(creators, list):
            for idx in creators:
                if isinstance(idx, dict):
                    for dict_key in idx.keys():
                        if dict_key not in creators_metadata.keys():
                            raise ValueError(
                                "The elements of the 'creators' list are dictionaries "
                                "with the following allowed keys:\n"
                                f"{json.dumps(list(creators_metadata.keys()), indent=4)}"
                            )
                else:
                    raise TypeError(
                        "Members of the creators list should be of dict type."
                    )
            tmp_metadata["creators"] = creators
        else:
            raise ValueError(
                "The 'creators' argument cannot be None and should be a list."
            )

        if description is not None and description != "":
            tmp_metadata["description"] = description
        else:
            raise ValueError("The 'description' argument cannot be None or empty.")

        if access_right is not None and access_right != "":
            if access_right in access_rights.keys():
                tmp_metadata["access_right"] = access_right
            else:
                raise ValueError(
                    "The 'access_right' value can take one of the following values:\n"
                    f"{json.dumps(list(access_rights.keys()), indent=4)}"
                )

            if access_right == "open" or access_right == "embargoed":
                if license is not None and license != "":
                    tmp_metadata["license"] = license
                else:
                    raise ValueError(
                        "The 'license argument cannot be None or empty if "
                        "'access_right' is 'open' or 'embargoed'."
                    )

            if access_right == "embargoed":
                if embargo_date is not None and embargo_date != "":
                    tmp_metadata["embargo_date"] = embargo_date
                else:
                    logger.warning(
                        "The 'embargo_date' argument cannot be None or empty...\n"
                        "Setting the 'embargo_date' to the current date."
                    )
                    tmp_metadata["embargo_date"] = (
                        datetime.now(timezone.utc).date().isoformat()
                    )
            elif access_right == "restricted":
                if access_conditions is not None and access_conditions != "":
                    tmp_metadata["access_conditions"] = access_conditions
                else:
                    raise ValueError(
                        "The 'access_conditions' argument cannot be None or empty."
                    )
        else:
            logger.warning(
                "The 'access_right' argument cannot be None or empty...\n"
                "Setting the 'access_right' to 'open'.\n"
            )
            tmp_metadata["access_right"] = "open"
            if upload_type == "dataset":
                logger.warning(
                    "The 'upload_type' == 'dataset'...\n"
                    "Setting the 'license' to 'cc-zero' (default).\n"
                )
                tmp_metadata["license"] = "cc-zero"
            else:
                logger.warning(
                    "The 'upload_type' != 'dataset'...\n"
                    "Setting the 'license' to 'cc-by' (default).\n"
                )
                tmp_metadata["license"] = "cc-by"

        tmp_data = {"metadata": tmp_metadata}
        response = requests.put(url=tmp_url, json=tmp_data, params=tmp_params)
        status_code = response.status_code
        if status_code != 200:
            # zenodo_error(status_code)
            request_error(response)
        return Record(self._client, record=response)
