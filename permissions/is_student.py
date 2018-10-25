import swapper

from rest_framework import permissions

from kernel.managers.get_role import get_role


class IsStudent(permissions.BasePermission):
    """
    Custom permission check for the user to be faculty member or not
    """

    def has_permission(self, request, view):
        """
        Permission to use Faculty App views
        """
        
        Student = swapper.load_model('kernel', 'Student')
        try:
            faculty = get_role(request.person, 'Student')
            return True
        except Student.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Permission to check whether the object handled by the faculty member 
        belongs to the faculty member
        """
        
        Student = swapper.load_model('kernel', 'Student')
        student = get_role(request.person, 'Student')
        if obj.student == student:
            return True
        else:
            return False




