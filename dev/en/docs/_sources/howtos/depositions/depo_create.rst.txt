.. _depo_create:

*********************************
How to Create an Empty Deposition
*********************************

.. note::
  
  Before going through this document, make sure you know how to create 
  an instance of the ``_Depositions`` class, **depo_obj**, by reviewing 
  the :ref:`deposition_howtos` guide.

In order to create an empty deposition form on our zenodo account,
call the ``create_deposition()`` function on an instance of the
``_Depositions`` class (here, the instance is stored in the **depo_obj** 
variable)

>>> my_depo = depo_obj.create_deposition()

Running this command not only creates an empty untitled
deposition form in your Zenodo account

.. figure:: ../../images/howtos/depo_create.png
  :align: center
  :alt: A freshly minted deposition form created by ``zenopy``

but also generates a deposition object of ``_Depositions`` type

>>> my_depo
<zenopy.depositions._Depositions at 0x7fe0da752bf0>

that can be further modified and submitted to Zenodo. 

You can directly access the contents of the **my_depo** deposition
object through its ``data`` attribute

>>> my_depo.data
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
  'publish': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185/actions/publish',
  'self': 'https://sandbox.zenodo.org/api/deposit/depositions/1112185'},
 'metadata': {'prereserve_doi': {'doi': '10.5072/zenodo.1112185',
   'recid': 1112185}},
 'modified': '2022-10-09T19:38:15.289650+00:00',
 'owner': 123811,
 'record_id': 1112185,
 'state': 'unsubmitted',
 'submitted': False,
 'title': ''}

.. tip::

  Each deposition is created with a unique identifier which you can access 
  through its ``_id`` attribute:

  >>> mydepo._id
  1112185

.. seealso::

   - :ref:`cli_client`