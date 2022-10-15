# -*- coding: utf-8 -*-

"""Zenodo Record class.

"""

from collections.abc import MutableMapping
import requests
import validators
import logging
import pprint
import inspect

logger = logging.getLogger(__name__)

class Record(MutableMapping):
    """Zenodo Record mixin container class"""

    def __init__(
        self, client, id_: int = None, url: str = None, record: (requests.models.Response | dict) = None
    ):
        self._base_url = client._base_url
        self._headers = client._headers
        self._params = client._params
        if id_ is not None and isinstance(id_, int):
            caller_class_name = str(inspect.currentframe().f_back.f_locals["self"])
            if "_Depositions" in caller_class_name:
                self._record_url = self._base_url + "/deposit/depositions/" + str(id_)
            elif "_DepositionFiles" in caller_class_name:
                self._record_url = self._base_url + "/deposit/depositions/" + str(id_) + "/files"
            # elif "_DepositionActions" in caller_class_name:
                # self._record_url = self._base_url + "/deposit/" + str(id_)
            else: # "_Records" (or anything else) in caller_class_name:
                self._record_url = self._base_url + "/records/" + str(id_)
            response = requests.get(
                self._record_url, params=self._params, headers=self._headers
            )
            self.data = response.json()
        elif url is not None and url != "":
            url = url.strip().rstrip("/")
            is_valid = validators.url(url)
            if is_valid:
                self._record_url = url
                response = requests.get(
                    self._record_url, params=self._params, headers=self._headers
                )
                self.data = response.json()
            else:
                raise ValueError(
                    f"The provided URL ({url}) is invalid.\n"
                    "Please enter a valid URL."
                )
        elif record is not None and record != {}:
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
            # Fetch the data whatever its nature or origin is (Deposit | Record)
            # The data comes either from "self" or "latest" in the "links" key
            if "self" in self.data[key].keys():
                self._record_url = self.data[key]["self"]
            else:
                self.data[key]["latest"]
        else:
            raise RuntimeError("Please provide a valid record URL, ID or object.")

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
            raise RuntimeError("The creation time of the record is not set.")

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
            raise ValueError("The DOI for the record cannot be empty or None.")

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
            raise ValueError("The DOI URL for the record cannot be empty or None.")

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
            raise RuntimeError("The (record-)id is not set or accessible.")

    @_id.setter
    def _id(self, idx: int = None) -> None:
        if idx is not None and isinstance(idx, int):
            self.data["id"] = int(idx)
            self.data["record_id"] = int(idx)
        else:
            raise TypeError(f"The record ID ({type(idx)}) is of invalid type.")

    @property
    def metadata(self) -> dict:
        """A deposition metadata resource."""
        if "metadata" in self.data and self.data["metadata"] != {}:
            return self.data["metadata"]
        else:
            raise RuntimeError("The record metadata is not set or accessible.")

    @property
    def modified(self) -> str:
        """Last modification time of the deposition/record (in ISO8601 format)."""
        if "modified" in self.data and self.data["modified"] != "":
            return self.data["modified"]
        elif "updated" in self.data and self.data["updated"] != "":
            return self.data["updated"]
        else:
            raise RuntimeError(
                "The last modification time of the record/deposition "
                "is not set or accessible."
            )

    @modified.setter
    def modified(self, date_modified: str = None) -> None:
        """Setting the last modification time of the deposition/record."""
        if date_modified is not None and date_modified != "":
            if "modified" in self.data and self.data["modified"] != "":
                self.data["modified"] = date_modified
            else:
                raise RuntimeError(
                    "The modification time of the deposition/record is not set or "
                    "accessible (unknown)."
                )
        else:
            raise ValueError(
                "The modification time for the record cannot be empty or None."
            )

    @property
    def owner(self) -> (int | list[int]):
        """User identifier(s) of the owner(s) of the deposition."""
        if "owner" in self.data and self.data["owner"] != "":
            return self.data["owner"]
        elif "owners" in self.data and self.data["owners"] != "":
            return self.data["owners"]
        else:
            raise RuntimeError(
                "The owner of the deposition/record is not set or "
                "accessible (unknown)."
            )

    @owner.setter
    def owner(self, owner_id: (int | list[int])) -> None:
        """User identifier(s) of the owner(s) of the deposition."""
        if owner_id is not None and owner_id != "":
            if isinstance(owner_id, int):
                self.data["owner"] = owner_id
            elif isinstance(owner_id, list):
                self.data["owner"] = owner_id[0]
                self.data["owners"] = owner_id
            else:
                raise TypeError(
                    "The provided user identifier is of invalid type "
                    f" ({type(owner_id)})."
                )
        else:
            raise ValueError(
                "The user identifier for the record cannot be empty or None."
            )

    @property
    def record_id(self) -> int:
        """Record identifier. This field is only present for published depositions."""
        for key in ["record_id", "id"]:
            if key in self.data and self.data[key] != "":
                return self.data[key]

        if "metadata" in self.data:
            if "prereserve_doi" in self.data["metadata"]:
                if (
                    "recid" in self.data["metadata"]["prereserve_doi"]
                    and self.data["metadata"]["prereserve_doi"]["recid"] != ""
                ):
                    return self.data["metadata"]["prereserve_doi"]["recid"]
        else:
            raise RuntimeError("The deposition/record identifier is unknown.")

    @property
    def record_url(self):
        """URL to public version of record for this deposition. This field is
        only present for published depositions."""
        if "record_url" in self.data and self.data["record_url"] != "":
            return self.data["record_url"]
        elif "links" in self.data and self.data["links"] != "":
            for key in [
                "self",
                "record",
                "record_html",
                "html",
                "latest",
                "latest_html",
            ]:
                if key in self.data["links"] and self.data["links"][key] != "":
                    return self.data["links"][key]
        else:
            raise RuntimeError(
                "The deposition/record URL is not accessible or unknown."
            )

    @property
    def state(self) -> str:
        """Zenodo publication state, either: (i) inprogress,
        (ii) done or (iii) error."""
        if "state" in self.data and self.data["state"] != "":
            # NOTE: The ["unsubmitted", "draft"] is not part of the official documentation but is in use in Zenodo
            if self.data["state"] in ["inprogress", "done", "unsubmitted", "draft"]:
                return self.data["state"]
            elif self.data["state"] == "error":
                raise RuntimeError(
                    "Deposition is in an error state - contact Zenodo support "
                    "at https://zenodo.org/support."
                )
            else:
                raise ValueError(
                    "The deposition state is set to an inappropriate value."
                )
        else:
            raise RuntimeError(
                "The state of the deposition is not set, accessible or known."
            )

    @property
    def submitted(self) -> bool:
        """A boolean value for submission state of the deposition:
        True if deposition has been published, False otherwise."""
        if "submitted" in self.data and self.data["submitted"] != "":
            return self.data["submitted"]
        else:
            raise RuntimeError(
                "The submission state of the deposition is not set, "
                "accessible or known."
            )

    @property
    def title(self) -> str:
        """Title of deposition (automatically set from metadata).
        Defaults to empty string."""
        if "title" in self.data and self.data["title"] != "":
            return self.data["title"]
        elif "metadata" in self.data:
            if (
                "title" in self.data["metadata"]
                and self.data["metadata"]["title"] != ""
            ):
                return self.data["metadata"]["title"]
        else:
            raise RuntimeError("The deposition title is not set, accessible or known.")

    @title.setter
    def title(self, title: str = "") -> None:
        """Set the deposition/record title."""
        if title is not None or title != "":
            self.data["title"] = title
            self.data["metadata"]["title"] = title
        else:
            raise ValueError(
                "The title argument value cannot be None or an empty string."
            )
