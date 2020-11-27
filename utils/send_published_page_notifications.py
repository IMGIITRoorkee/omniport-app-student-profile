from django.conf import settings

from notifications.actions import push_notification

from categories.models import Category


def send_published_page_notification(person, enrolment_no):
    """
    :param person:
    :param enrolment_no:
    :return:
    """

    service = settings.DISCOVERY.get_app_configuration(
        'student_profile'
    )
    category, _ = Category.objects.get_or_create(
        name=service.nomenclature.verbose_name,
        slug=service.nomenclature.name,
    )
    push_notification(
        template=f'Your page on "https://students.iitr.ac.in/{enrolment_no}.html" has been published.',
        category=category,
        web_onclick_url='',
        android_onclick_activity='',
        ios_onclick_action='',
        is_personalised=True,
        person=person.id,
        has_custom_users_target=False,
        persons=None,
    )
