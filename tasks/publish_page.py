import requests

from omniport.celery import celery_app

celery_app.control.add_consumer('shp_publish', reply=True)


@celery_app.task(
    queue='shp_publish'
)
def publish_page(full_name, enrollment_no, shp_publish_endpoint):
    """
    :param full_name: Full name of the student.
    :param enrollment_no: Enrollment no of the student.
    :param shp_publish_endpoint: Endpoint for SHP publish main worker.

    :return: Publishes page with given enrollment_no
    """

    student_data = {
        'enrollment_no': enrollment_no,
        'full_name': full_name,
    }

    try:
        requests.post(shp_publish_endpoint, data=student_data, timeout=15)
    except:
        pass
