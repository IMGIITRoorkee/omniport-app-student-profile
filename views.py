import swapper
import logging

from django.db import transaction, IntegrityError
from django.db.models import FieldDoesNotExist, Q
from django.core.exceptions import ObjectDoesNotExist, ValidationError, ImproperlyConfigured
from django.utils.datastructures import MultiValueDictKeyError

from itertools import chain
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from formula_one.models.generics.social_information import SocialLink
from formula_one.serializers.generics.social_information import SocialLinkSerializer
from kernel.managers.get_role import get_role
from kernel.permissions.has_role import get_has_role
from omniport.settings.configuration.base import CONFIGURATION

from student_profile.permissions.is_student import IsStudent
from student_profile.serializers.generic_serializers import common_dict
from student_profile.serializers.student_serializer import StudentSearchSerializer
from student_profile.tasks.publish_page import publish_page

logger = logging.getLogger('student_profile')

Student = swapper.load_model('kernel', 'Student')

models = {}
for key in common_dict:
    models[key] = swapper.load_model('student_biodata', key)


def return_viewset(class_name):
    """
    A generic function used to generate viewsets for every model.
    """

    class Viewset(ModelViewSet):
        """
        API endpoint that allows models to be viewed or edited.
        """

        serializer_class = common_dict[class_name]["serializer"]
        permission_classes = (get_has_role('Student'), )
        pagination_class = None
        filter_backends = tuple()

        def get_queryset(self):
            Model = models[class_name]
            try:
                student = get_role(self.request.person, 'Student')
            except:
                return []
            options = ['priority', 'semester',  'year', 'start_date', 'id']
            for option in options[:]:
                try:
                    Model._meta.get_field(option)
                except FieldDoesNotExist:
                    options.remove(option)
            return Model.objects.order_by(*options).filter(student=student)

        def exception_handler(func):
            """
            Decorator to add exception handling to create and update methods.
            :param func: function to apply this decorator over

            :return: a function which raises an error if the passed function
            raises an error
            """

            def raise_error(*args, **kwargs):
                """
                Wrapper function to raise error
                """

                try:
                    return func(*args, **kwargs)
                except IntegrityError as error:
                    return Response(
                        {'Fatal error': [error.__cause__.diag.message_detail]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except ValidationError as error:
                    return Response(
                        error.message_dict,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return raise_error

        @exception_handler
        def create(self, request, *args, **kwargs):
            """
            Modify create method to catch errors
            """

            return super().create(request, *args, **kwargs)

        def perform_create(self, serializer):
            """
            modifying perform_create for all the views to get Student
            instance from request
            """

            student = get_role(self.request.person, 'Student')
            serializer.save(student=student)

        @exception_handler
        def update(self, request, *args, **kwargs):
            """
            Modify update method to catch errors
            """

            return super().update(request, *args, **kwargs)

        def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            class_name = instance.__class__.__name__
            if class_name == "PreviousEducation" or class_name == "CurrentEducation":
                if instance.verified is True:
                    return Response("Cannot delete verified education instances", status.HTTP_403_FORBIDDEN)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        @action(detail=True, methods=['get'], permission_classes=[])
        def handle(self, request, pk=None):
            """
            providing an open endpoint for showing the data for normal users
            """

            Model = models[class_name]
            Profile = models['Profile']
            profile = None

            try:
                profile = Profile.objects.get(handle=pk)
            except ObjectDoesNotExist:
                return Response(status=404,)
            student = profile.student
            options = ['priority', 'semester', 'start_date', 'id']
            for option in options[:]:
                try:
                    Model._meta.get_field(option)
                except FieldDoesNotExist:
                    options.remove(option)
            objects = Model.objects.order_by(
                *options).filter(student=student, visibility=True)
            return Response(self.get_serializer(objects, many=True).data)

    return Viewset


class SocialLinkViewSet(ModelViewSet):
    """
    API endpoint that allows SocialLink Model to be viewed or edited.
    """

    permission_classes = (get_has_role('Student'), )
    serializer_class = SocialLinkSerializer
    pagination_class = None

    def get_queryset(self):
        person = self.request.person
        if person is not None:
            socialinformation = person.social_information.filter()
        else:
            return []
        if len(socialinformation) != 0:
            queryset = SocialLink.objects.filter(
                socialinformation=socialinformation[0]
            )
        else:
            queryset = []
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

    @action(detail=True, methods=['get'], permission_classes=[])
    def handle(self, request, pk=None):
        """
        providing an open endpoint fot showing the data for normal users
        """

        Model = SocialLink
        Profile = models['Profile']
        profile = None
        try:
            profile = Profile.objects.get(handle=pk)
        except ObjectDoesNotExist:
            return Response(status=404,)
        student = profile.student
        options = ['priority', 'semester', 'start_date', 'id']
        for option in options[:]:
            try:
                Model._meta.get_field(option)
            except FieldDoesNotExist:
                options.remove(option)
        social_info = student.person.social_information.first()
        links = social_info.links if social_info else list()
        return Response(SocialLinkSerializer(links, many=True).data)


for key in common_dict:
    common_dict[key]["viewset"] = return_viewset(key)


class ProfileViewset(ModelViewSet):
    """
    API endpoint that allows models to be viewed or edited.
    """

    serializer_class = common_dict['Profile']['serializer']
    permission_classes = (get_has_role('Student'), )
    pagination_class = None
    filter_backends = tuple()

    def get_queryset(self):
        Model = models['Profile']
        try:
            student = get_role(self.request.person, 'Student')
        except:
            return []
        profile = Model.objects.order_by('-id').filter(student=student)
        if len(profile) == 0:
            profile = Model.objects.create(
                student=student, handle=student.enrolment_number, description="Student at IITR")
            profile.save()
            return [profile]
        return profile

    def create(self, request, *args, **kwargs):
        """
        Modifying create method to add functionality of adding profile image
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        person = request.person
        try:
            img_file = request.data['image']
            if img_file is None or img_file == "null":
                person.display_picture = None
                person.save()
            else:
                person.display_picture.save(img_file.name, img_file, save=True)
        except MultiValueDictKeyError:
            logger.info('MultiValueDictKeyError has occurred \
                when user tried to upload profile image')
        try:
            data['displayPicture'] = request.person.display_picture.url
        except ValueError:
            data['displayPicture'] = None
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        modifying perform_create for all the views to get Student
        instance from request
        """

        student = get_role(self.request.person, 'Student')
        serializer.save(student=student)

    def update(self, request, *args, **kwargs):
        """
        modifying update function to change image field to null in case of deleting the profile image
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        parser_class = (MultiPartParser, )
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data = serializer.data
        try:
            img_file = request.data['image']
            person = request.person
            if img_file is None or img_file == "null":
                person.display_picture = None
                person.save()
            else:
                person.display_picture.save(img_file.name, img_file, save=True)
        except MultiValueDictKeyError:
            logger.info('MultiValueDictKeyError has occurred \
                when user tried to upload profile image')
        try:
            data['displayPicture'] = request.person.display_picture.url
        except ValueError:
            data['displayPicture'] = None
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        """
        modifying destroy method to remove only the resume field
        """

        instance = self.get_object()
        instance.resume = None
        instance.save()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[])
    def handle(self, request, pk=None):
        """
        A view to get the profile information without the authentication
        """

        try:
            profile = models['Profile'].objects.get(handle=pk)
            data = self.get_serializer(profile).data
            try:
                data['displayPicture'] = profile.student.person.display_picture.url
            except ValueError:
                data['displayPicture'] = None
            data['fullName'] = profile.student.person.full_name
        except ObjectDoesNotExist:
            return Response(status=404,)

        return Response(data)


common_dict['Profile']["viewset"] = ProfileViewset


class StudentSearchList(generics.ListAPIView):
    """
    View to return the student search list.
    """

    serializer_class = StudentSearchSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get('query', None)

        students = Student.objects.filter(
            Q(enrolment_number__icontains=query) | 
            Q(profile__handle__icontains=query) | 
            Q(person__full_name__icontains=query)
        ).order_by('enrolment_number')[:10]

        result = list(chain(students))
        return result


class PublishPageView(APIView):
    """
    API endpoint to publish a preview page
    """

    permission_classes = (get_has_role('Student'), )
    SHP = CONFIGURATION.integrations.get('shp', False)

    def check_configuration(self):
        if self.SHP:
            attributes = [
                self.SHP.get('shp_publish_endpoint')
            ]
            if all(attributes):
                return True
            else:
                raise ImproperlyConfigured
        else:
            return False

    def get(self, request):
        """
        Returns whether SHP configuration exists or not
        :return: whether SHP configuration exists or not
        """

        try:
            is_configured = self.check_configuration()
            if is_configured:
                return Response(
                    'SHP configuration detected',
                    status=status.HTTP_200_OK,
                )
            return Response(
                'You probably do not need students page published',
                status=status.HTTP_404_NOT_FOUND,
            )
        except ImproperlyConfigured:
            return Response(
                (
                    'SHP falsely configured. Please provide `shp_publish_endpoint` '
                    'in the configuration'
                ),
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

    def post(self, request):
        try:
            is_configured = self.check_configuration()
        except ImproperlyConfigured:
            return Response(
                (
                    'SHP falsely configured. Please provide `shp_publish_endpoint` '
                    'in the configuration'
                ),
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        if is_configured:
            data = request.data
            handle = data['handle']
            enrolment_number = request.person.student.enrolment_number
            shp_endpoint = self.SHP.get('shp_publish_endpoint')

            publish_page.delay(handle, enrolment_number, shp_endpoint)
            return Response(
                "Successfully added to publish queue",
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                'You probably do not need students page published',
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )


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
        model_name = data['model']
        Model = models[model_name]
        objects = Model.objects.order_by('id').filter(student=student)
        serializer = common_dict[model_name]['serializer']
        priority_array = data['order']
        if(len(priority_array) == len(objects)):
            order = dict()
            for i in range(len(priority_array)):
                order[priority_array[i]] = i + 1
            for obj in objects:
                obj.priority = order[obj.id]
                obj.save()
        return Response(serializer(objects.order_by('priority'), many=True).data)
