.. _file_create:

*******************************
How to Create a Deposition File
*******************************

.. note::
  
  Before going through this document, please ensure that you know how 
  to create an instance of the ``_DepositionFiles`` class, **depo_file_obj**,
  by reviewing the :ref:`files_howtos` guide.

In order to upload a file from disk to a deposition form on your
Zenodo account, you will need two pieces of information: (i) a
absolute or relative ``file_path`` to an existing file on disk that 
you want to upload to your deposition form, and (ii) a ``bucket_url``
which will be the link to our deposition's file container on the Zenodo
server. Let's store these information into some variables:

>>> fpath  = "./test.txt"
>>> buckurl = "https://sandbox.zenodo.org/api/files/6c5452f3-66d6-4f34-9040-e9a48a079b19"

Now, you can simply call the ``create_deposition_file()`` function on 
an instance of the ``_DepositionFiles`` class (here, the instance is
stored in the **depo_file_obj** variable) and pass the aforementioned
variables as function arguments

>>> my_depo_file = depo_file_obj.create_deposition_file(file_path=fpath, bucket_url=buckurl)
>>> my_depo_file
<zenopy.record.Record at 0x7f1590da73a0>

.. note::

  Since the ``bucket_url`` embeds the information about the deposition ID, there is no 
  need to pass that information to the ``create_deposition_file()`` function as an argument.

We can look at the content of the **my_depo_file** object

>>> my_depo_file.data
{'mimetype': 'text/plain',
 'updated': '2022-10-16T16:16:54.406753+00:00',
 'links': {'self': 'https://sandbox.zenodo.org/api/files/6c5452f3-66d6-4f34-9040-e9a48a079b19/test.txt',
  'version': 'https://sandbox.zenodo.org/api/files/6c5452f3-66d6-4f34-9040-e9a48a079b19/test.txt?versionId=cca11f5b-344f-47f2-873c-42487b4f9b7e',
  'uploads': 'https://sandbox.zenodo.org/api/files/6c5452f3-66d6-4f34-9040-e9a48a079b19/test.txt?uploads'},
 'is_head': True,
 'created': '2022-10-16T16:16:54.397452+00:00',
 'checksum': 'md5:e19c1283c925b3206685ff522acfe3e6',
 'version_id': 'cca11f5b-344f-47f2-873c-42487b4f9b7e',
 'delete_marker': False,
 'key': 'test.txt',
 'size': 15}

Checking back our our Zenodo account, we can see that the **test.txt** file
has been uploaded to the deposition form.

.. figure:: ../../images/howtos/file_create.png
  :align: center
  :alt: A test text file uploaded to the deposition form by ``zenopy``

.. tip::

  The ``bucket_url`` can be extracted from the ``links`` field of the
  ``data`` attribute in our deposition or record object. See
  the :ref:`depo_list` or :ref:`depo_retrieve` guides for examples
  on how to inspect the contents of a deposition via its ``data`` attribute.

.. seealso::

  - :ref:`files_howtos` 
  - :ref:`depo_list`
  - :ref:`depo_retrieve`