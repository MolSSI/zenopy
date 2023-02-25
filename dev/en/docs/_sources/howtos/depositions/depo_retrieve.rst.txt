.. _depo_retrieve:

*****************************************************
How to Retrieve a Deposition from your Zenodo Account
*****************************************************

.. note::
  
  Before going through this document, make sure you know how to create 
  an instance of the ``_Depositions`` class, **depo_obj**, by reviewing 
  the :ref:`deposition_howtos` guide.

An existing deposition can be retrieved from your zenodo account by passing
its unique ID to the ``retrieve_deposition()`` function provided by 
the ``_Depositions`` class

>>> depo = depo_obj.retrieve_deposition(id_=1112185)

Here, we have fetched the deposition corresponding to the ``id_ = 1112185``.
Let's make sure we have fetched the correct deposition

>>> depo.data
{'conceptrecid': '1112184',
 'created': '2022-10-09T19:38:15.289636+00:00',
 'files': [],
 'id': 1112185,
 'links': {'bucket': 'https://sandbox.zenodo.org/api/files/a67735cf-1d9e-41de-8555-9d1dbec72177',
  'discard': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/actions/discard',
  'edit': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/actions/edit',
  'files': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/files',
  'html': 'https://sandbox.zenodo.org/deposit/1112185',
  'latest_draft': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185',
  'latest_draft_html': 'https://sandbox.zenodo.org/deposit/1112185',
  'newversion': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/actions/newversion',
  'publish': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/actions/publish',
  'registerconceptdoi': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/actions/registerconceptdoi',
  'self': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185'},
 'metadata': {'prereserve_doi': {'doi': '10.5072/zenodo.1112185',
   'recid': 1112185}},
 'modified': '2022-10-09T19:38:15.289650+00:00',
 'owner': 123811,
 'record_id': 1112185,
 'state': 'unsubmitted',
 'submitted': False,
 'title': ''}

You can find the pertinent ID in the **id** entry of the dictionary. You can also access it 
through the ``_id`` attribute of the retrieved deposition object (**depo**)

>>> depo._id
1112185

.. seealso::

  - :ref:`depo_create`
  - :ref:`depo_list`