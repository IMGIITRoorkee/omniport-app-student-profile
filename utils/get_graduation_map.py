def get_graduation(graduation_constant):
    """
    :param graduation_constant:
    :return: different representation of graduation
    """

    graduation_map = {
        'gra': 'UG',
        'pos': 'PG',
        'doc': 'PhD',
    }
    if graduation_constant in graduation_map.keys():
        return graduation_map[graduation_constant]
    else:
        return None
