# -*- coding: utf-8 -*-

"""Zenodo Deposition class metadata container class member with
controlled vocabulary

"""

from datetime import datetime, timezone
from collections import UserDict

upload_types = {
    "publication": "Publication",
    "poster": "Poster",
    "presentation": "Presentation",
    "dataset": "Dataset",
    "image": "Image",
    "video": "Video/Audio",
    "software": "Software",
    "lesson": "Lesson",
    "physicalobject": "Physical object",
    "other": "Other",
}

# if upload_type == "publication"
publication_types = {
    "annotationcollection": "Annotation collection",
    "book": "Book",
    "section": "Book section",
    "conferencepaper": "Conference paper",
    "datamanagementplan": "Data management plan",
    "article": "Journal article",
    "patent": "Patent",
    "preprint": "Preprint",
    "deliverable": "Project deliverable",
    "milestone": "Project milestone",
    "proposal": "Proposal",
    "report": "Report",
    "softwaredocumentation": "Software documentation",
    "taxonomictreatment": "Taxonomic treatment",
    "technicalnote": "Technical note",
    "thesis": "Thesis",
    "workingpaper": "Working paper",
    "other": "Other",
}

# if upload_type == "image"
image_types = {
    "figure": "Figure",
    "plot": "Plot",
    "drawing": "Drawing",
    "diagram": "Diagram",
    "photo": "Photo",
    "other": "Other",
}

creators = {
    "name": "Name of creator in the format Family name, Given names",
    "affiliation": "Affiliation of creator (optional)",
    "orcid": "ORCID identifier of creator (optional)",
    "gnd": "GND identifier of creator (optional)",
}

class Creators(UserDict):


class MetaData(UserDict):
    """Container class for Deposition metadata."""
    def __init__(
        self,
        upload_type: str = None,
        publication_date: str = None,
        title: str = None,
        creators: 
    ):
        self.upload_type = upload_type.lower()
        if publication_date is None or publication_date == "":
            self.publication_date = datetime.now(timezone.utc).date().isoformat()
        if title is None or title == "":
            self.title = ""

