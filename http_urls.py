from django.conf.urls import url, include
from rest_framework import routers
import inflection
from student_profile.views import  SocialLinkViewSet, DragAndDropView
from student_profile.serializers.generic_serializers import common_dict

app_name = 'student_profile'

router = routers.DefaultRouter()

for model in common_dict:
    router.register(
        inflection.underscore(model),
        common_dict[model]["viewset"],
        base_name=model,
    )

router.register(r'social_link',SocialLinkViewSet,base_name="SocialLink")

urlpatterns = [
    url(r'rearrange', DragAndDropView.as_view()),
    url(r'^', include(router.urls)),
]
