.. _user_guide_client:

*************
zenopy Client
*************

The ``Zenodo`` client class in ``zenopy`` is the main gate to its functionality
providing a secure and efficient communication route to your private or public
records available on Zenodo repositories.

Public records on Zenodo are freely available to and impose no restrictions on
the user accounts. Thus, users can easily use ``zenopy`` to search through 
the existing public records published Zenodo or query their metadata. 

Contrary to accessing the public records, Zenodo requires you to create a 
private token from your Zenodo account if you plan to interact with your 
personal/organization data repositories on Zenodo servers.

Zenodo offers a brief `tutorial <https://developers.zenodo.org/#authentication>`_ 
on how to create a token from your account. We will repeat it here for the 
sake of completeness:

.. attention::

    All API requests must be authenticated and submitted over HTTPS. Any request
    transferred over plain HTTP will fail. Zenodo supports authentication via 
    OAuth 2.0.

.. note::
    In order to create a personal access token:

      #. `Register <https://zenodo.org/signup>`_ for a Zenodo account if you don't already
         have one.
      #. Go to your `Applications <https://zenodo.org/account/settings/applications>`_,
         to `create a new token <https://zenodo.org/account/settings/applications/tokens/new>`_.
      #. Select the OAuth scopes you need (for the quick start tutorial you need 
         ``deposit:write`` and ``deposit:actions``).

.. attention::

    Do not share your personal access token with anyone else and only use it 
    over HTTPS.

