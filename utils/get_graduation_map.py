from kernel.constants.graduations import GRADUATE, POSTGRADUATE, DOCTORATE


def get_graduation(graduation_constant):
    """
    :param graduation_constant:
    :return: different representation of graduation
    """

    graduation_map = {
        GRADUATE: 'UG',
        POSTGRADUATE: 'PG',
        DOCTORATE: 'PhD',
    }
    if graduation_constant in graduation_map.keys():
        return graduation_map[graduation_constant]
    else:
        return None
