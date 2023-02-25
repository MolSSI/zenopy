.. _cli_token:

*************************************
How to Create an Authentication Token
*************************************

An authentication token is similar to a password that allows you get access 
to your devices. Once created, you do not normally share it with others 
and keep it somewhere safe.

In order to create a Zenodo (Sandbox) account token, login to your account and 
navigate to the **Applications** tab from your profile menu
(top-right corner of your screen)

.. figure:: ../../images/howtos/token_applications.png
  :align: center
  :alt: Navigating to the Applications tab

In the Applications page, you should be able to see a list of all tokens
created using your account in the **Personal access tokens** tab.

.. figure:: ../../images/howtos/token_new_token.png
  :align: center
  :alt: The Applications page

Click on the **+ New token** button on the top-right corner of the same section
to be directed to a new page that looks like he one shown below

.. figure:: ../../images/howtos/token_create.png
  :align: center
  :alt: Labeling a token with various permission levels

This page allows you pick a name for your access token and assign various 
permission levels or **scopes** to your token. Simply pick the scope you need
and click on the blue button **create**. You will then be automatically taken
to another page that has your personal token in it written in red 
(redacted in the picture below)

.. figure:: ../../images/howtos/token_store.png
  :align: center
  :alt: The generated token to be stored in a config file

Congratulations! You can now use this token to access your account through
``zenopy`` package.

.. tip::

    Although not necessary, we recommend choosing token names that clarify their
    scope and account type (Sandbox or not). In this example, we have picked the
    label **MYTOKEN_ALL_SB** which clarifies its name (MYTOKEN), scope 
    (ALL: ``deposit:actions``, ``deposit:write`` and ``user:email``) 
    and account type (SB: ``Sandbox``).

.. danger::

    Do not close the final web page that has your token in it until you
    have stored it in your config file. You will not be able to access this
    token from your account after closing this page.

.. seealso::

   - :ref:`cli_config`
   - :ref:`cli_client`