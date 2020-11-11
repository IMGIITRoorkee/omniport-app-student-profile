import requests

from omniport.celery import celery_app

from omniport.settings.configuration.base import CONFIGURATION

SHP = CONFIGURATION.integrations.get('SHP')

celery_app.control.add_consumer('shp_publish', reply=True)


@celery_app.task(
    queue='shp_publish'
)
def publish_page(full_name, enrollment_no):
    """
    :return: Publishes page with given enrollment_no
    """

    SHP_PUBLISH_ENDPOINT = SHP.get('shp_publish_endpoint')
    student_data = {
        'enrollment_no': enrollment_no,
        'full_name': full_name,
    }

    try:
        requests.post(SHP_PUBLISH_ENDPOINT, data=student_data, timeout=15)
    except:
        pass
