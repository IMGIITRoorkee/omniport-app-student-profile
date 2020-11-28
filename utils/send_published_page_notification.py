from django.conf import settings

from categories.models import Category
from notifications.actions import push_notification


def send_published_page_notification(person, enrolment_no, shp_url):
    """
    :param person:
    :param enrolment_no:
    :param shp_url:
    :return:
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
        person=person.id,
        has_custom_users_target=False,
        persons=None
    )
