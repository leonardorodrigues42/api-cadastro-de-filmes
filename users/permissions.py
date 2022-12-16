from rest_framework import permissions

class EmployeePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_employee or request.user == obj  
    

class EmployeeRestrictPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_employee
