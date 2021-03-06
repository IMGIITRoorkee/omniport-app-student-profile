from student_profile.utils.get_int_to_roman import int_to_roman
from student_profile.utils.get_graduation_map import get_graduation


def get_decorated_degree_with_graduation(student):
    """
    Get decorated degree like 'UG (II Year II Semester)'
    """
    degree_grad = get_graduation(student.branch.degree.graduation[0])
    current_year = student.current_year
    current_semester = 1 if student.current_semester % 2 else 2
    decorated_degree = (
        f'{degree_grad} ({int_to_roman(current_year)} Year '
        f'{int_to_roman(current_semester)} Semester)'
    )
    return decorated_degree
