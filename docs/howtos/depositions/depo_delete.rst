.. _depo_delete:

***************************************
How to Delete an Unpublished Deposition
***************************************

.. note::
  
  Before going through this document, make sure you know how to create 
  an instance of the ``_Depositions`` class, **depo_obj**, by reviewing 
  the :ref:`deposition_howtos` guide.

An **unpublished** deposition can be deleted from your Zenodo account
by calling the ``delete_deposition()`` from an instance of the 
``_Depositions`` class. Here, we plan to delete a deposition
with the ID value of **1112185** as shown below

>>> depo_obj.delete_deposition(id_=1112185)
An unpublished deposition has been deleted at the following address:
	https://sandbox.zenodo.org/api/deposit/depositions/

The printed statement verifies that the target deposition has been
successfully deleted from your account.

.. attention::

  Once you have **published** a deposition, you will not be able to update 
  or delete it using ``update_deposition()`` or ``delete_deposition()``, respectively.
  In order to delete or update a published deposition `contact the Zenodo 
  Support Team <https://zenodo.org/support>`_.

.. seealso::

  - :ref:`depo_create`
  - :ref:`depo_retrieve`
  - :ref:`depo_update`