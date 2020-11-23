import requests

from omniport.celery import celery_app

celery_app.control.add_consumer('shp_publish', reply=True)


@celery_app.task(
    queue='shp_publish'
)
def publish_page(enrolment_no, shp_publish_endpoint, shp_publish_token):
    """
    :param enrolment_no: Enrolment no of the student.
    :param shp_publish_endpoint: Endpoint for SHP publish main worker.
    :param shp_publish_token: Token for SHP publish main worker.

    :return: Publishes page with given enrolment_no
    """

    student_data = {
        'enrolment_no': enrolment_no,
    }

    try:
        requests.post(
            shp_publish_endpoint,
            headers={
                'SHP_TOKEN': shp_publish_token,
            },
            data=student_data,
            timeout=15
        )
    except requests.Timeout:
        raise Exception('Timeout exceeded more than 15secs.')
    except Exception as error:
        raise Exception(f'Request unsuccessful. Error: {str(error)}')