.. _file_list:

********************************
How to List the Deposition Files
********************************

.. note::
  
  Before going through this document, please ensure that you know how 
  to create an instance of the ``_DepositionFiles`` class, **depo_file_obj**,
  by reviewing the :ref:`files_howtos` guide.

In this guide, we work on a new version draft of a deposition uploaded
to our Zenodo account with the record ID = 1114771 (see below)

.. figure:: ../../images/howtos/file_create.png
  :align: center
  :alt: The deposition form page corresponding to the deposition ID = 1114771

We can get a list of all files uploaded to the deposition with the deposition
ID = 1114771 as

>>> depo_file_list = depo_file_obj.list_deposition_files(id_=1114771)
>>> depo_file_list
[<zenopy.record.Record at 0x7fca505505b0>,
 <zenopy.record.Record at 0x7fca487b7a90>]

Having a list of deposition files stored in the variable **depo_file_list**,
we can print the file name and file IDs of every member in the list as follows

.. code-block::

  >>> for f in depo_file_list:
  >>>     print("[Filename]: %s; \n[File ID]: %s\n" % (f.get("filename"), f.get("id")))
    [Filename]: sample2.txt; 
    [File ID]: 5dfbf589-a8f7-4853-81d8-1b03665f19bf

    [Filename]: test.txt; 
    [File ID]: 21077a2a-d716-48a9-89e5-9b4d0465863a

The **File IDs** can be used to retrieve single deposition files. See the 
:ref:`file_retrieve` guide.

.. seealso::

  - :ref:`files_howtos`
  - :ref:`file_create`
  - :ref:`depo_list`
  - :ref:`depo_retrieve`