from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from rest_framework import routers, viewsets, permissions

from rpm.models import Repository

# Permissions
class IsOwnerOrGeneralAccess(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if settings.GENERAL_ACCESS:
            return bool(request.user and request.user.is_authenticated())
        else:
            if request.user and request.user.is_authenticated():
                view.queryset = Repository.objects.filter(owner=request.user)
                return True
            else:
                return False

    def has_object_permission(self, request, view, obj):
        if settings.GENERAL_ACCESS:
            return bool(request.user and request.user.is_authenticated())
        else:
            if isinstance(obj, Repository):
                return obj.owner == request.user
            else:
                return False

# ViewSets
class RepositoryViewSet(viewsets.ModelViewSet):
    model = Repository
    queryset = Repository.objects.all()
    permission_classes = (IsOwnerOrGeneralAccess,)

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)