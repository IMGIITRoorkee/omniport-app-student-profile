from django.conf.urls import url, include
from rest_framework import routers
import inflection

from student_profile.views import SocialLinkViewSet, DragAndDropView, StudentSearchList
from student_profile.serializers.generic_serializers import common_dict

app_name = 'student_profile'

router = routers.DefaultRouter()

for model in common_dict:
    router.register(
        inflection.underscore(model),
        common_dict[model]["viewset"],
        basename=model,
    )

router.register(r'social_link',SocialLinkViewSet,basename="SocialLink")

urlpatterns = [
    url(r'rearrange', DragAndDropView.as_view()),
    url(r'search_students', StudentSearchList.as_view()),
    url(r'^', include(router.urls)),
]
