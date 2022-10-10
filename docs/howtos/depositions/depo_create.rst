.. _depo_create:

**************************
How to Create a Deposition
**************************

In order to create an empty deposition form template on 
your zenodo account, you need to take three steps:

#. Create a ``zenopy`` client object
#. Construct a ``Deposition`` object
#. Call the ``create_deposition()`` function

Let's begin by importing the ``zenopy`` package,

>>> import zenopy

This enables you to call the ``Zenodo()`` constructor
to get a handle to the client object

>>> cli = zenopy.Zenodo()
WARNING: The config file (~/.zenodorc) is found.

The warning will tell you that ``zenopy`` client is now
connected to your Zenodo account. You can now call the 
client object's ``init_deposition()`` function to construct 
an instance of the ``Deposition`` class.

>>> depo_obj = cli.init_deposition()

The **depo_obj** object allows you to create, update, list, delete *etc.*
the depositions on your Zenodo account. Let's use it to create an
empty deposition form on our zenodo account and store it into an object
that we can later on update or submit to our Zenodo account.

>>> my_depo = depo.obj.create_deposition()
>>> my_depo
<zenopy.depositions._Depositions at 0x7fe0da752bf0>

This command has two effects:

- It creates an untitled freshly minted deposition form template in 
  your Zenodo account



- AS

We can inspect what information is stored in the 
**my_depo** deposition objectfor 

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

