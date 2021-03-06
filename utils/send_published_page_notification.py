from django.conf import settings

from categories.models import Category
from notifications.actions import push_notification


def send_published_page_notification(person, enrolment_no, shp_url):
    """
    :param person: Person whom to be notified
    :param enrolment_no: Enrolment no used for publishing page
    :param shp_url: Url for Student's home page
    :return: Send a notification for published page
    """

    service = settings.DISCOVERY.get_app_configuration(
        'student_profile'
    )
    category, _ = Category.objects.get_or_create(
        name=service.nomenclature.verbose_name,
        slug=service.nomenclature.name,
    )

    page_url = f'{shp_url}/{enrolment_no}.html'

    push_notification(
        template=f'Your page on "{page_url}" has been published.',
        category=category,
        web_onclick_url=page_url,
        android_onclick_activity='',
        ios_onclick_action='',
        is_personalised=True,
        person=person,
        has_custom_users_target=False,
        persons=None
    )
