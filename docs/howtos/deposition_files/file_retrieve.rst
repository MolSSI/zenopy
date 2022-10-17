.. _file_retrieve:

*********************************
How to Retrieve a Deposition File
*********************************

.. note::
  
  Before going through this document, please ensure that you know how 
  to create an instance of the ``_DepositionFiles`` class, **depo_file_obj**,
  by reviewing the :ref:`files_howtos` guide.

In this guide, we plan to retrieve the **test.txt** from a draft deposition
in our Zenodo Sandbox account. 

.. figure:: ../../images/howtos/file_create.png
  :align: center
  :alt: The deposition form page corresponding to the deposition ID = 1114771

We need two pieces of information: (i) the deposition ID (here, ID = 1114771),
and (ii) the file ID (in this case, File ID: 21077a2a-d716-48a9-89e5-9b4d0465863a).
Let's store these two IDs in two separate variables for convenience:

>>> depo_id = 1114771
>>> file_id = "21077a2a-d716-48a9-89e5-9b4d0465863a"

Now, you can simply call the ``retrieve_deposition_file()`` function on 
an instance of the ``_DepositionFiles`` class (here, the instance is
stored in the **depo_file_obj** variable) and pass the aforementioned
variables as function arguments

>>> my_depo_file = depo_file_obj.retrieve_deposition_file(id_=1114771, file_id="21077a2a-d716-48a9-89e5-9b4d0465863a")
>>> my_depo_file
<zenopy.record.Record at 0x7fca48359900>

Let's check the file name of the deposition file stored in the
**my_depo_file** variable

>>> my_depo_file.get("filename")
'test.txt'

which shows we have received the file we were looking for.

.. seealso::

  - :ref:`files_howtos` 
  - :ref:`file_list`
  - :ref:`file_create`