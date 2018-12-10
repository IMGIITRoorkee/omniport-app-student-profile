from django.conf.urls import url, include
from rest_framework import routers
import inflection
from student_profile.views import viewset_dict, new_viewset_dict, SocialLinkViewSet
from student_profile.views import DragAndDropView, RefereeViewSet

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
]

router = routers.DefaultRouter()
# require authentication

for model in models:
    router.register(
        inflection.underscore(model),
        viewset_dict[model],
        base_name=model,
    )

# only require enrolment number
# router.register(r'test/(?P<enr_no>[^/.]+'),viewset_dict["Paper"],base_name="base")
# for model in models:

#     router.register(
#         inflection.underscore(model)+(r'/?P<enr_no>[0-9]+$'),
#         new_viewset_dict[model],
#         base_name=model,
#     )


router.register(r'social_link', SocialLinkViewSet, base_name="SocialLink")
router.register(r'referee', RefereeViewSet, base_name="Referee")
urlpatterns = [
    url(r'rearrange', DragAndDropView.as_view()),
    url(r'^', include(router.urls))
]
