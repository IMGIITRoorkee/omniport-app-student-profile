from django.conf.urls import url, include
from rest_framework import routers
import inflection
from student_profile.views import viewset_dict, SocialLinkViewSet
from student_profile.views import DragAndDropView

models = [
    'CurrentEducation',
    'PreviousEducation',
    'Achievement',
    'Experience',
    'Position',
    'Project',
    'Interest',
    'Skill',
    'Profile',
    'Book',
    'Paper',
    'Referee',
]

router = routers.DefaultRouter()


for model in models:
    router.register(
        inflection.underscore(model),
        viewset_dict[model],
        base_name=model,
    )
router.register(r'social_link', SocialLinkViewSet, base_name="SocialLink")
urlpatterns = [
    url(r'rearrange', DragAndDropView.as_view()),
    url(r'^', include(router.urls))
]
