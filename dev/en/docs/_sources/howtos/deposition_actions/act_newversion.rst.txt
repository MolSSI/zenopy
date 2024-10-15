.. _act_newversion:

******************************************************
How to Create a New Version for a Published Deposition
******************************************************

.. note::
  
  Before going through this document, make sure you know how to create 
  an instance of the ``_DepositionActions`` class, **depo_act_obj**,
  by reviewing the :ref:`actions_howtos` guide.

We start with a published deposition (ID = 1097408) in the Zenodo Sandbox
account. A new version of the deposition can be created from either **published**
or **draft** states. In the former case, once you click on the deposition
title

.. figure:: ../../images/howtos/act_edit_1.png
  :align: center
  :alt: An already published mock deposition in a Zenodo account

you will be navigated to the content page where you can find the green
**New version** button on the top-right corner of the screen.

.. figure:: ../../images/howtos/act_edit_2.png
  :align: center
  :alt: The content page of an already published mock deposition in a Zenodo account

If the deposition is in the **draft** state, clicking on its title will redirect
you to the deposition form page

.. figure:: ../../images/howtos/act_discard.png
  :align: center
  :alt: The form page of a draft deposition

where you can find the green **New version** button at the center of the
**Files** section of the form . Regardless of the deposition
state, ``zenopy`` allows you to create a new version for your record
programmatically by by calling the ``deposition_action()`` function 
on an instance of the ``_DepositionActions`` class and passing 
``action = 'newversion'`` as an argument

>>> my_depo = depo_act_obj.deposition_action(id_=1097408, action='newversion')
>>> my_depo
<zenopy.record.Record at 0x7f62a450a860>

Now, we can inspect the contents of the new version of the record 
stored in the **my_repo** variable

>>> my_depo.data
Output exceeds the size limit. Open the full output data in a text editor
{'conceptdoi': '10.5072/zenodo.1095981',
 'conceptrecid': '1095981',
 'created': '2022-10-16T03:40:36.736949+00:00',
 'doi': '10.5072/zenodo.1114771',
 'doi_url': 'https://doi.org/10.5072/zenodo.1114771',
 'files': [{'checksum': 'cd375ecc07df759665a323de96e06237',
   'filename': 'sample2.txt',
   'filesize': 23,
   'id': '5dfbf589-a8f7-4853-81d8-1b03665f19bf',
   'links': {'download': 'https://sandbox.zenodo.org/api/files/6c5452f3-66d6-4f34-9040-e9a48a079b19/sample2.txt',
    'self': 'https://sandbox.zenodo.org/api/deposit/depositions/1114771/files/5dfbf589-a8f7-4853-81d8-1b03665f19bf'}}],
 'id': 1114771,
 'links': {'badge': 'https://sandbox.zenodo.org/badge/doi/10.5072/zenodo.1114771.svg',
  'bucket': 'https://sandbox.zenodo.org/api/files/6c5452f3-66d6-4f34-9040-e9a48a079b19',
  'conceptbadge': 'https://sandbox.zenodo.org/badge/doi/10.5072/zenodo.1095981.svg',
  'conceptdoi': 'https://doi.org/10.5072/zenodo.1095981',
  'discard': 'https://sandbox.zenodo.org/api/deposit/depositions/1114771/actions/discard',
  'doi': 'https://doi.org/10.5072/zenodo.1114771',
  'edit': 'https://sandbox.zenodo.org/api/deposit/depositions/1114771/actions/edit',
  'files': 'https://sandbox.zenodo.org/api/deposit/depositions/1114771/files',
  'html': 'https://sandbox.zenodo.org/deposit/1114771',
  'latest': 'https://sandbox.zenodo.org/api/records/1097408',
  'latest_draft': 'https://sandbox.zenodo.org/api/deposit/depositions/1114771',
  'latest_draft_html': 'https://sandbox.zenodo.org/deposit/1114771',
  'latest_html': 'https://sandbox.zenodo.org/record/1097408',
...
 'owner': 123811,
 'record_id': 1114771,
 'state': 'unsubmitted',
 'submitted': False,
 'title': 'My New Title'}

And finally, we can double-check the ID of the new version of our deposition

>>> my_depo._id
1114771

.. attention::

  A new version for a deposition should only be created when you plan to
  add new files or remove or modify the existing files in our published
  deposition. For other changes such as changing metadata, you should
  edit and publish the same deposition version.

.. important::

  When a new version of an existing deposition is created, a new DOI
  will also be assigned to it.

.. seealso::

  - :ref:`actions_howtos`
  - :ref:`act_edit`
  - :ref:`act_discard`
  - :ref:`act_publish`
  - :ref:`deposition_howtos`