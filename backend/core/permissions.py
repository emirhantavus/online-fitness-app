from rest_framework import permissions
from programs.models import Evolution , TrainerStudentProgram

class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.groups.filter(name='moderators').exists())

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user 
    
    
class IsTrainer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_trainer

class IsStudentOrTrainer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Evolution):
            return request.user == obj.exercise.program.student or request.user.is_trainer
        if isinstance(obj, TrainerStudentProgram):
            return request.user == obj.student or request.user == obj.trainer or request.user.is_staff
        return False
    