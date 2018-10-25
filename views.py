import swapper

from rest_framework.viewsets import ModelViewSet

from kernel.managers.get_role import get_role
from student_profile.serializers import serializer_dict
from student_profile.permissions.is_student import IsStudent

viewset_dict = {
    'CurrentEducation' : None,
    'PreviousEducation' : None,
    'Achievement' : None,
    'Experience' : None,
    'Position' : None,
    'Project' : None,
    'Interest' : None,
    'Skill' : None,
    'Profile' : None,
    'Book' : None,
    'Paper' : None,
}

def return_viewset(class_name):
    class Viewset(ModelViewSet):
        """
        API endpoint that allows models to be viewed or edited.
        """
        serializer_class = serializer_dict[class_name]
        permission_classes = (IsStudent, )
        pagination_class = None
        filter_backends = tuple()

        def get_queryset(self):
            Model = swapper.load_model('student_biodata', class_name)
            student = get_role(self.request.person, 'Student')
            return Model.objects.filter(student=student)

        def perform_create(self, serializer):
            """
            modifying perform_create for all the views to get Student
            instance from request
            """
            student = get_role(self.request.person, 'Student')
            serializer.save(student=student)
            
    return Viewset


for key in serializer_dict:
    viewset_dict[key] = return_viewset(key)

