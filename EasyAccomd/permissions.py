from rest_framework.permissions import BasePermission

class ViewAndChangePermission(BasePermission):
    def has_object_permission(self, request, view, object):
        return(object.email==request.user.email)

class IsRenter(BasePermission):
    def has_object_permission(self, request, view, object):
        return(request.user.user_type=='renter')

class IsHost(BasePermission):
    def has_object_permission(self, request, view, object):
        return(request.user.user_type=='host')
        
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, object):
        return(object.host_of_this_post==request.user)