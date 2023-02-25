.. _rec_retrieve:

**************************************
How to Retrieve a Public Zenodo Record
**************************************

.. note::
  
  Before going through this document, make sure you know how to create 
  an instance of the ``_Records`` class, **rec_obj**, by reviewing 
  the :ref:`records_howtos` guide.

In order to be able to retrieve a public record, you need to pass its ID to the 
``retrieve_record()`` as an argument. Let's fetch the *Fundamentals of Heterogeneous
Parallel Programming with CUDA C/C++* workshop tutorials (ID: 5389982) from Zenodo:

.. code-block:: python

  >>> my_record = rec_obj.retrieve_record(id_=5389982)
  >>> my_record
  <zenopy.record.Record at 0x7fb2806a3d00>

Now that we have the record stored in the **my_record** variable, we can check its title

.. code-block:: python

  >>> my_record.title
  'MolSSI Formatting Guidelines for Machine Learning Products'

or inspect its content

.. code-block:: python

  >>> my_record.data
  Output exceeds the size limit. Open the full output data in a text editor
  {'conceptdoi': '10.5281/zenodo.5389981',
   'conceptrecid': '5389981',
   'created': '2021-09-02T16:41:11.277319+00:00',
   'doi': '10.5281/zenodo.5389982',
   'files': [{'bucket': '6b6e5721-930a-46bf-80ad-15a1ff35e23b',
     'checksum': 'md5:32daf9cba263bbce5c4f744bd62f2558',
     'key': 'ML_Formatting_Guidelines.odt',
     'links': {'self': 'https://zenodo.org/api/files/6b6e5721-930a-46bf-80ad-15a1ff35e23b/ML_Formatting_Guidelines.odt'},
     'size': 21001,
     'type': 'odt'},
    {'bucket': '6b6e5721-930a-46bf-80ad-15a1ff35e23b',
     'checksum': 'md5:185ea215c01d4f44a2c398cbe8856214',
     'key': 'ML_Formatting_Guidelines.pdf',
     'links': {'self': 'https://zenodo.org/api/files/6b6e5721-930a-46bf-80ad-15a1ff35e23b/ML_Formatting_Guidelines.pdf'},
     'size': 92394,
     'type': 'pdf'}],
   'id': 5389982,
   'links': {'badge': 'https://zenodo.org/badge/doi/10.5281/zenodo.5389982.svg',
    'bucket': 'https://zenodo.org/api/files/6b6e5721-930a-46bf-80ad-15a1ff35e23b',
    'conceptbadge': 'https://zenodo.org/badge/doi/10.5281/zenodo.5389981.svg',
    'conceptdoi': 'https://doi.org/10.5281/zenodo.5389981',
    'doi': 'https://doi.org/10.5281/zenodo.5389982',
    'html': 'https://zenodo.org/record/5389982',
    'latest': 'https://zenodo.org/api/records/5389982',
    'latest_html': 'https://zenodo.org/record/5389982',
    ...
    'version_views': 98.0,
    'version_volume': 5564641.0,
    'views': 98.0,
    'volume': 5564641.0},
   'updated': '2022-01-20T22:14:12.141358+00:00'}

.. seealso::

   - :ref:`records_howtos`
   - :ref:`rec_list`