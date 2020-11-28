import requests
from http import HTTPStatus

from omniport.celery import celery_app

from student_profile.utils.send_published_page_notification import (
    send_published_page_notification
)

celery_app.control.add_consumer('shp_publish', reply=True)


@celery_app.task(
    queue='shp_publish'
)
def publish_page(person, enrolment_no, shp_publish_endpoint, shp_publish_token, shp_url):
    """
    :param person: Person who has requested for published page.
    :param enrolment_no: Enrolment no of the student.
    :param shp_publish_endpoint: Endpoint for SHP publish main worker.
    :param shp_publish_token: Token for SHP publish main worker.
    :param shp_url: Url for student home page

    :return: Publishes page with given enrolment_no
    """

    student_data = {
        'enrolment_no': enrolment_no,
    }

    try:
        publish_request = requests.post(
            shp_publish_endpoint,
            headers={
                'SHP_TOKEN': shp_publish_token,
            },
            data=student_data,
            timeout=20
        )
    except requests.Timeout:
        raise Exception('Timeout exceeded more than 20secs.')
    except Exception as error:
        raise Exception(f'Request unsuccessful. Error: {str(error)}')

    if publish_request.status_code == HTTPStatus.CREATED:
        send_published_page_notification(
            person,
            enrolment_no,
            shp_url
        )
