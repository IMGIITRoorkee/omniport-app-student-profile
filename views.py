import swapper
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from kernel.managers.get_role import get_role
from kernel.permissions.has_role import get_has_role
from student_profile.serializers.generic_serializers import (
    serializer_dict,
)
from student_profile.serializers.social_link import SocialLinkSerializer
from kernel.models.generics.social_information import SocialLink
from student_profile.permissions.is_student import IsStudent


viewset_dict = {
    'CurrentEducation': None,
    'PreviousEducation': None,
    'Achievement': None,
    'Experience': None,
    'Position': None,
    'Project': None,
    'Interest': None,
    'Skill': None,
    'Profile': None,
    'Book': None,
    'Paper': None,
}


def return_viewset(class_name):
    class Viewset(ModelViewSet):
        """
        API endpoint that allows models to be viewed or edited.
        """
        serializer_class = serializer_dict[class_name]
        permission_classes = (get_has_role('Student'), )
        pagination_class = None
        filter_backends = tuple()

        def get_queryset(self):
            Model = swapper.load_model('student_biodata', class_name)
            student = get_role(self.request.person, 'Student')
            return Model.objects.order_by('-id').filter(student=student)

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


class SocialLinkViewSet(ModelViewSet):
    """
    API endpoint that allows SocialLink Model to be viewed or edited.
    """
    permission_classes = (get_has_role('Student'), )
    serializer_class = SocialLinkSerializer
    pagination_class = None

    def get_queryset(self):
        person = self.request.person
        socialinformation = person.social_information.filter()
        if len(socialinformation) !=0 :
            queryset = SocialLink.objects.filter(
            socialinformation=socialinformation[0]
        )
        else:
            queryset=[]
        return queryset

    def perform_create(self, serializer):
        """
        modifying perform_create for all the views to get Student
        instance from request
        """
        person = self.request.person
        link_instance = serializer.save()
        si, created = person.social_information.get_or_create()
        person.social_information.all()[0].links.add(link_instance)

class ProfileViewset(ModelViewSet):
        """
        API endpoint that allows models to be viewed or edited.
        """
        serializer_class = serializer_dict['Profile']
        permission_classes = (get_has_role('Student'), )
        pagination_class = None
        filter_backends = tuple()

        def get_queryset(self):
            Model = swapper.load_model('student_biodata', 'Profile')
            student = get_role(self.request.person, 'Student')
            return Model.objects.order_by('-id').filter(student=student)

        def perform_create(self, serializer):
            """
            modifying perform_create for all the views to get Student
            instance from request
            """
            student = get_role(self.request.person, 'Student')
            serializer.save(student=student)
        
        def destroy(self, request, *args, **kwargs):
            """
            modifying destroy method to remove only the resume field
            """
            
            instance = self.get_object()
            instance.resume = None
            instance.save()
            serializer = self.get_serializer(instance)
            
            return Response(serializer.data)
    
viewset_dict['Profile'] = ProfileViewset


class DragAndDropView(APIView):
        """
        API endpoint that allows the changing if the ordering of the models
        """
        
        permission_classes = (get_has_role('Student'), )
        pagination_class = None
        filter_backends = ()

        @transaction.atomic
        def post(self, request):
            data = request.data
            student = get_role(self.request.person, 'Student')
            modelName = data['model']
            Model = swapper.load_model('student_biodata', modelName)
            objects = Model.objects.order_by('id').filter(student=student)
            serializer = serializer_dict[modelName]
            priority_array  = data['order']
            if(len(priority_array) == len(objects)):
                order = dict()
                for i in range(len(priority_array)):
                    order[priority_array[i]] = i
                for obj in objects:
                    obj.priority = order[obj.id]
                    obj.save()
            return Response(serializer(objects.order_by('priority'), many=True).data)

        

