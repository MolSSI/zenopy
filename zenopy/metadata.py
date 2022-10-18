# -*- coding: utf-8 -*-

"""Zenodo Deposition class metadata container class member with
controlled vocabulary

"""


access_rights = {
    "open": "Open Access",
    "embargoed": "Embargoed Access",
    "restricted": "Restricted Access",
    "closed": "Closed Access",
}

creators_metadata = {
    "name": "Name of creator in the format Family name, Given names",
    "affiliation": "Affiliation of creator (optional)",
    "orcid": "ORCID identifier of creator (optional)",
    "gnd": "GND identifier of creator (optional)",
}

deposition_actions = {
    "publish": (
        "Publish a deposition. Note, once a deposition is published, "
        "you can no longer delete it."
    ),
    "edit": "Unlock already submitted deposition for editing.",
    "discard": "Discard changes in the current editing session.",
    "newversion": (
        "Create a new version of a deposition.\n\nThis action will "
        "create a new deposit, which will be a snapshot of the current resouce, "
        "inheriting the metadata as well as snapshot of files. The new version deposit "
        "will have a state similar to a new, unpublished deposit, most importantly its "
        "files will be modifiable as for a new deposit.\n\nOnly one unpublished new "
        "version deposit can be available at any moment, i.e.: calling new version action "
        "multiple times will have no effect, as long as the resulting new version deposit "
        "from the first call is not published or deleted.\n\nNOTES: - The response body of "
        "this action is NOT the new version deposit, but the original resource. The new "
        "version deposition can be accessed through the 'latest_draft' under 'links' in "
        "the response body. - The id used to create this new version has to be the id of "
        "the latest version. It is not possible to use the global id that references all "
        "the versions."
    ),
}

funder_dois = {
    "Australian Research Council": "10.13039/501100000923",
    "Austrian Science Fund": "10.13039/501100002428",
    "European Commission": "10.13039/501100000780",
    "European Environment Agency": "10.13039/501100000806",
    "Academy of Finland": "10.13039/501100002341",
    "Hrvatska Zaklada za Znanost": "10.13039/501100004488",
    "Fundação para a Ciência e a Tecnologia": "10.13039/501100001871",
    "Ministarstvo Prosvete, Nauke i Tehnološkog Razvoja": "10.13039/501100004564",
    "Ministarstvo Znanosti, Obrazovanja i Sporta": "10.13039/501100006588",
    "National Health and Medical Research Council": "10.13039/501100000925",
    "National Institutes of Health": "10.13039/100000002",
    "National Science Foundation": "10.13039/100000001",
    "Nederlandse Organisatie voor Wetenschappelijk Onderzoek": "10.13039/501100003246",
    "Research Councils": "10.13039/501100000690",
    "Schweizerischer Nationalfonds zur Förderung der wissenschaftlichen Forschung": "10.13039/501100001711",
    "Science Foundation Ireland": "10.13039/501100001602",
    "Wellcome Trust": "10.13039/100004440",
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

records_query_arguments = {
    "q": {
        "required": False,
        "condition": None,
        "description": "Search query (using Elasticsearch query string syntax).",
    },
    "status": {
        "required": False,
        "condition": None,
        "description": (
            "Filter result based on the deposit status (either draft " "or published)"
        ),
    },
    "sort": {
        "required": False,
        "condition": None,
        "description": (
            "Sort order (bestmatch or mostrecent). Prefix with minus "
            "to change form ascending to descending (e.g. -mostrecent)."
        ),
    },
    "page": {
        "required": False,
        "condition": None,
        "description": "Page number for pagination",
    },
    "size": {
        "required": False,
        "condition": None,
        "description": "Number of results to return per page",
    },
    "all_versions": {
        "required": False,
        "condition": None,
        "description": "Show (true or 1) or hide (false or 0) all versions of records",
    },
    "communities": {
        "required": False,
        "condition": None,
        "description": (
            "Return records that are part of the specified communities. "
            "(Use of community identifier)"
        ),
    },
    "type": {
        "required": False,
        "condition": None,
        "description": (
            "Return records of the specified type. (Publication, "
            "Poster, Presentation…)"
        ),
    },
    "subtype": {
        "required": False,
        "condition": None,
        "description": (
            "Return records of the specified subtype. (Journal "
            "article, Preprint, Proposal…)"
        ),
    },
    "bounds": {
        "required": False,
        "condition": None,
        "description": (
            "Return records filtered by a geolocation bounding box. "
            "(Format bounds=143.37158,-38.99357,146.90918,-37.35269)"
        ),
    },
    "custom": {
        "required": False,
        "condition": None,
        "description": (
            "Return records containing the specified custom keywords. "
            "(Format custom=[field_name]:field_value)"
        ),
    },
}

records_search_headers = {
    "json": "application/json",
    "zenodo": "application/vnd.zenodo.v1+json",
    "marcxml": "application/marcxml+xml",
    "bibtex": "application/x-bibtex",
    "datacitexml": "application/x-datacite+xml",
    "dublincore": "application/x-dc+xml",
}

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

# ========== metadata ==========
metadata = {
    "upload_type": {
        "required": True,
        "condition": None,
        "description": upload_types,
    },
    "publication_type": {
        "required": True,
        "condition": "'upload_type' == 'publication'",
        "description": publication_types,
    },
    "image_type": {
        "required": True,
        "condition": "'upload_type' == 'image'",
        "description": image_types,
    },
    "publication_date": {
        "required": True,
        "condition": None,
        "description": (
            "Date of publication in ISO8601 format (YYYY-MM-DD). "
            "Defaults to current date."
        ),
    },
    "title": {
        "required": True,
        "condition": None,
        "description": "Title of deposition",
    },
    "creators": {
        "required": True,
        "condition": None,
        "description": creators_metadata,
    },
    "description": {
        "required": True,
        "condition": None,
        "description": "Abstract or description for deposition.",
    },
    "access_right": {
        "required": True,
        "condition": None,
        "description": access_rights,
    },
    "license": {
        "required": True,
        "condition": "'access_right' == 'open' or 'access_right' == 'embargoed'",
        "description": (
            "The selected license applies to all files in this deposition, "
            "but not to the metadata which is licensed under Creative Commons Zero. "
            "You can find the available license IDs via our /api/licenses endpoint. "
            "Defaults to cc-zero for datasets and cc-by for everything else."
        ),
    },
    "embargo_date": {
        "required": True,
        "condition": "'access_right' == 'embargoed'",
        "description": (
            "When the deposited files will be made automatically made "
            "publicly available by the system. Defaults to current date."
        ),
    },
    "access_conditions": {
        "required": True,
        "condition": "'access_right' == 'restricted'",
        "description": (
            "Specify the conditions under which you grant users access "
            "to the files in your upload. User requesting access will be asked to justify "
            "how they fulfil the conditions. Based on the justification, you decide who to "
            "grant/deny access. You are not allowed to charge users for granting access to "
            "data hosted on Zenodo."
        ),
    },
    "doi": {
        "required": False,
        "condition": None,
        "description": (
            "Digital Object Identifier. Did a publisher already assign a "
            "DOI to your deposited files? If not, leave the field empty and we will register "
            "a new DOI for you when you publish. A DOI allow others to easily and "
            "unambiguously cite your deposition."
        ),
    },
    "prereserve_doi": {
        "required": False,
        "condition": None,
        "description": (
            "Set to true, to reserve a Digital Object Identifier (DOI). "
            "The DOI is automatically generated by our system and cannot be changed. "
            "Also, The DOI is not registered with DataCite until you publish your deposition, "
            "and thus cannot be used before then. Reserving a DOI is useful, if you need "
            "to include it in the files you upload, or if you need to provide a dataset DOI "
            "to your publisher but not yet publish your dataset. The response from the "
            "REST API will include the reserved DOI."
        ),
    },
    "keywords": {
        "required": False,
        "condition": None,
        "description": (
            "Free form keywords for this deposition. "
            "Example: ['Keyword 1', 'Keyword 2']"
        ),
    },
    "notes": {
        "required": False,
        "condition": None,
        "description": "Additional notes",
    },
    "related_identifiers": {
        "required": False,
        "condition": None,
        "description": (
            "Persistent identifiers of related publications and datasets. "
            "Supported identifiers include: DOI, Handle, ARK, PURL, ISSN, ISBN, PubMed ID, "
            "PubMed Central ID, ADS Bibliographic Code, arXiv, Life Science Identifiers (LSID), "
            "EAN-13, ISTC, URNs and URLs. Each array element is an object with the attributes:\n"
            "   * identifier: The persistent identifier\n"
            "   * relation: Relationship. Controlled vocabulary (isCitedBy, cites, isSupplementTo, "
            "isSupplementedBy, isContinuedBy, continues, isDescribedBy, describes, hasMetadata, "
            "isMetadataFor, isNewVersionOf, isPreviousVersionOf, isPartOf, hasPart, isReferencedBy, "
            "references, isDocumentedBy, documents, isCompiledBy, compiles, isVariantFormOf, "
            "isOriginalFormof, isIdenticalTo, isAlternateIdentifier, isReviewedBy, reviews, "
            "isDerivedFrom, isSourceOf, requires, isRequiredBy, isObsoletedBy, obsoletes).\n"
            "   * resource_type: Type of the related resource (based on the upload_type, "
            "publication_type, and image_type fields).\n\n"
            "Example: [{'relation': 'isSupplementTo', 'identifier':'10.1234/foo'}, "
            "{'relation': 'cites', 'identifier':'https://doi.org/10.1234/bar', "
            "'resource_type': 'image-diagram'}]. Note the identifier type (e.g. DOI) is "
            "automatically detected, and used to validate and normalize the identifier into "
            "a standard form."
        ),
    },
    "contributors": {
        "required": False,
        "condition": None,
        "description": (
            "The contributors of the deposition (e.g. editors, data curators, "
            "etc.). Each array element is an object with the attributes:\n\n"
            "* name: Name of creator in the format Family name, Given names\n"
            "* type: Contributor type. Controlled vocabulary (ContactPerson, "
            "DataCollector, DataCurator, DataManager,Distributor, Editor, Funder, "
            "HostingInstitution, Producer, ProjectLeader, ProjectManager, ProjectMember, "
            "RegistrationAgency, RegistrationAuthority, RelatedPerson, Researcher, ResearchGroup, "
            "RightsHolder,Supervisor, Sponsor, WorkPackageLeader, Other)\n"
            "* affiliation: Affiliation of creator (optional).\n"
            "* orcid: ORCID identifier of creator (optional).\n"
            "* gnd: GND identifier of creator (optional).\n\n"
            "Example: [{'name':'Doe, John', 'affiliation': 'Zenodo', 'type': 'Editor' }, ...]"
        ),
    },
    "references": {
        "required": False,
        "condition": None,
        "description": (
            "List of references.\n\n"
            "Example: ['Doe J (2014). Title. Publisher. DOI', 'Smith J (2014). Title. Publisher. DOI']"
        ),
    },
    "communities": {
        "required": False,
        "condition": None,
        "description": (
            "List of communities you wish the deposition to appear. The owner of the "
            "community will be notified, and can either accept or reject your request. Each array "
            "element is an object with the attributes:\n"
            "* identifier: Community identifier\n\nExample: [{'identifier':'ecfunded'}]"
        ),
    },
    "grants": {
        "required": False,
        "condition": None,
        "description": (
            "List of OpenAIRE-supported grants, which have funded the research for "
            "this deposition. Each array element is an object with the attributes:\n"
            "* id: grant ID.\n\nExample: [{'id':'283595'}] (European Commission grants only) or funder "
            "DOI-prefixed: [{'id': '10.13039/501100000780::283595'}] (All grants, recommended)\n\n"
            "Accepted funder DOI prefixes:\n"
            "Australian Research Council: 10.13039/501100000923\n"
            "Austrian Science Fund: 10.13039/501100002428\n"
            "European Commission: 10.13039/501100000780\n"
            "European Environment Agency: 10.13039/501100000806\n"
            "Academy of Finland: 10.13039/501100002341\n"
            "Hrvatska Zaklada za Znanost: 10.13039/501100004488\n"
            "Fundação para a Ciência e a Tecnologia: 10.13039/501100001871\n"
            "Ministarstvo Prosvete, Nauke i Tehnološkog Razvoja: 10.13039/501100004564\n"
            "Ministarstvo Znanosti, Obrazovanja i Sporta: 10.13039/501100006588\n"
            "National Health and Medical Research Council: 10.13039/501100000925\n"
            "National Institutes of Health: 10.13039/100000002\n"
            "National Science Foundation: 10.13039/100000001\n"
            "Nederlandse Organisatie voor Wetenschappelijk Onderzoek: 10.13039/501100003246\n"
            "Research Councils: 10.13039/501100000690\n"
            "Schweizerischer Nationalfonds zur Förderung der wissenschaftlichen Forschung: 10.13039/501100001711\n"
            "Science Foundation Ireland: 10.13039/501100001602\n"
            "Wellcome Trust: 10.13039/100004440"
        ),
    },
    "journal_title": {
        "required": False,
        "condition": "'upload_type' == 'publication'",
        "description": "Journal title",
    },
    "journal_volume": {
        "required": False,
        "condition": "'upload_type' == 'publication'",
        "description": "Journal volume",
    },
    "journal_issue": {
        "required": False,
        "condition": "'upload_type' == 'publication'",
        "description": "Journal issue",
    },
    "journal_page": {
        "required": False,
        "condition": "'upload_type' == 'publication'",
        "description": "Journal page",
    },
    "conference_title": {
        "required": False,
        "condition": None,
        "description": (
            "Title of conference (e.g. 20th International Conference on Computing "
            "in High Energy and Nuclear Physics)"
        ),
    },
    "conference_acronym": {
        "required": False,
        "condition": None,
        "description": "Acronym of conference (e.g. CHEP'13).",
    },
    "conference_dates": {
        "required": False,
        "condition": None,
        "description": (
            "Dates of conference (e.g. 14-18 October 2013). "
            "Conference title or acronym must also be specified if this field is specified."
        ),
    },
    "conference_place": {
        "required": False,
        "condition": None,
        "description": (
            "Place of conference in the format city, country (e.g. Amsterdam, The "
            "Netherlands). Conference title or acronym must also be specified if this field "
            "is specified."
        ),
    },
    "conference_url": {
        "required": False,
        "condition": None,
        "description": "URL of conference (e.g. http://www.chep2013.org/).",
    },
    "conference_session": {
        "required": False,
        "condition": None,
        "description": "Number of session within the conference (e.g. VI).",
    },
    "conference_session_part": {
        "required": False,
        "condition": None,
        "description": "Number of part within a session (e.g. 1)",
    },
    "imprint_publisher": {
        "required": False,
        "condition": None,
        "description": "Publisher of a book/report/chapter",
    },
    "imprint_isbn": {
        "required": False,
        "condition": None,
        "description": "ISBN of a book/report",
    },
    "imprint_place": {
        "required": False,
        "condition": None,
        "description": "Place of publication of a book/report/chapter in the format city, country",
    },
    "partof_title": {
        "required": False,
        "condition": None,
        "description": "Title of book for chapters",
    },
    "partof_pages": {
        "required": False,
        "condition": None,
        "description": "Pages numbers of book",
    },
    "thesis_supervisors": {
        "required": False,
        "condition": None,
        "description": "Supervisors of the thesis. Same format as for 'creators'",
    },
    "thesis_university": {
        "required": False,
        "condition": None,
        "description": "Awarding university of thesis",
    },
    "subjects": {
        "required": False,
        "condition": None,
        "description": (
            "Specify subjects from a taxonomy or controlled vocabulary. "
            "Each term must be uniquely identified (e.g. a URL). For free form text, use "
            "the keywords field. Each array element is an object with the attributes:\n"
            "* term: Term from taxonomy or controlled vocabulary.\n"
            "* identifier: Unique identifier for term.\n"
            "* scheme: Persistent identifier scheme for id (automatically detected).\n\n"
            "Example: [{'term': 'Astronomy', 'identifier': "
            "'http://id.loc.gov/authorities/subjects/sh85009003', 'scheme': 'url'}]"
        ),
    },
    "version": {
        "required": False,
        "condition": None,
        "description": (
            "Version of the resource. Any string will be accepted, "
            "however the suggested format is a semantically versioned tag (see more details "
            "on semantic versioning at semver.org)\nExample: 2.1.5"
        ),
    },
    "language": {
        "required": False,
        "condition": None,
        "description": (
            "Specify the main language of the record as ISO 639-2 or 639-3 "
            "code, see Library of Congress ISO 639 codes list.\nExample: eng"
        ),
    },
    "locations": {
        "required": False,
        "condition": None,
        "description": (
            "List of locations\n"
            "* lat (double): latitude\n"
            "* lon (double): longitude\n"
            "* place (string): place’s name (required)\n"
            "* description (string): place’s description (optional)\n"
            "Example: [{'lat': 34.02577, 'lon': -118.7804, 'place': 'Los Angeles'}, "
            "{'place': 'Mt.Fuji, Japan', 'description': "
            "'Sample found 100ft from the foot of the mountain.'}]"
        ),
    },
    "dates": {
        "required": False,
        "condition": None,
        "description": (
            "List of date intervals:\n"
            "* start (ISO date string): start date (*)\n"
            "* end (ISO date string): end date (*)\n"
            "* type (Collected, Valid, Withdrawn): The interval’s type (required)\n"
            "* description (string): The interval’s description (optional)\n"
            "(*) Note that you have to specify at least a start or end date. For "
            "an exact date, use the same value for both 'start' and 'end'.\n"
            "Example: [{'start': '2018-03-21', 'end': '2018-03-25', "
            "'type': 'Collected', 'description': 'Specimen A5 collection period'}]"
        ),
    },
    "method": {
        "required": False,
        "condition": None,
        "description": "The methodology employed for the study or research.",
    },
}
