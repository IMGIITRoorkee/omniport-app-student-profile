from django.urls import re_path, include
from rest_framework import routers
import inflection

from student_profile.views import (
    SocialLinkViewSet, 
    DragAndDropView,
    PublishPageView, 
    StudentSearchList,
)
from student_profile.serializers.generic_serializers import common_dict

app_name = 'student_profile'

router = routers.DefaultRouter()

for model in common_dict:
    router.register(
        inflection.underscore(model),
        common_dict[model]["viewset"],
        basename=model,
    )

router.register(r'social_link', SocialLinkViewSet, basename="SocialLink")

urlpatterns = [
    re_path(r'publish', PublishPageView.as_view()),
    re_path(r'rearrange', DragAndDropView.as_view()),
    re_path(r'search_students', StudentSearchList.as_view()),
    re_path(r'^', include(router.urls)),
]
