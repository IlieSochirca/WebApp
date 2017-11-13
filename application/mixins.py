from django.conf import settings
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from .models import *


class UserAuthorMixin(object):
    # This MIXIN whill check if the user if the author of a group or a block of smth. If not, error 403 will be displayed and he can't do any action towards this group.
    def dispatch(self, request, *args, **kwargs):
        if request.user.id is not self.get_object().added_by.id:
            raise PermissionDenied
        return super(UserAuthorMixin, self).dispatch(request, *args,**kwargs)

class UserAuthorMixinPost(object):
    # This MIXIN whill check if the user if the author of a group or a block of smth. If not, error 403 will be displayed and he can't do any action towards this group.
    def dispatch(self, request, *args, **kwargs):
        if request.user.id is not self.get_object().posted_by.id:
            raise PermissionDenied
        return super(UserAuthorMixinPost, self).dispatch(request, *args,**kwargs)

#
# class UserAuthenticationMixin(object):
#     # We are checking here if the user is authenticated. If yes, we continue to dispatch, if not, we are going to send him to login page
#
#     def dispatch(self, request, *args, **kwargs):
