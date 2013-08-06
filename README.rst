MyYUM
=====

MyYUM is a web-based YUM repository manager, where each user can manage his own set of YUM repository completly from within his web browser. It supports creation of repositories and upload and removal of packages.

Using Windows Azure Storage
---------------------------

It's very simple when using the pyazure library. Put the following into your localsettings.py:

.. code:: python
    DEFAULT_FILE_STORAGE = "pyazure.storage.django_storage.AzureBlockStorage"
    MEDIA_URL = 'http://yum-store.02strich.de/yum/'
    AZURE_FILES = {
        'account_name': 'yumdev',
        'key': os.environ['AZURE_KEY'],
        'container_name': 'yum',
        'base_url': 'http://yum-store.02strich.de/'
    }

Using Django-Social-Auth
------------------------

This project is prepared to be used with django-social-auth. Just enable the backend you plan to use and drop in the respective credentials. If you plan on using a provider beyond Google, Yahoo or GitHub please also add the respective button in the templates/login.html.

In order to enable GitHub login, for example, add the following lines to your localsettings.py:

.. code:: python
    import os

    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.contrib.github.GithubBackend',
    )

    GITHUB_APP_ID     = os.environ['GITHUB_CLIENTID']
    GITHUB_API_SECRET = os.environ['GITHUB_SECRET']

Using LDAP auth
---------------

In an enterprise setting LDAP auth is probably more interesting and can be achieved in the following way. First install the django-auth-ldap package. Then put the following into your localsettings.py:

.. code:: python

    import ldap
    from django_auth_ldap.config import LDAPSearch

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    AUTH_LDAP_SERVER_URI = "ldap://10.41.68.201"

    AUTH_LDAP_BIND_DN = ""
    AUTH_LDAP_BIND_PASSWORD = ""
    AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=figo,dc=me", ldap.SCOPE_SUBTREE, "(cn=%(user)s)")

    AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn"}
