
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