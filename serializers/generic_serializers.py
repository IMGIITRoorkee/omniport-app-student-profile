import swapper

from rest_framework import serializers

serializer_dict = {
    'CurrentEducation': None,
    'PreviousEducation': None,
    'Achievement': None,
    'Experience': None,
    'Position': None,
    'Project': None,
    'Interest': None,
    'Skill': None,
    'Profile': None,
    'Book': None,
    'Paper': None,
    'Referee':None
}


def return_serializer(class_name):
    """
    Return the serializer for the given class
    :param class_name: the class whose serializer is being generated
    """

    class Serializer(serializers.ModelSerializer):
        """
        Serializer for given class name
        """

        student = serializers.ReadOnlyField(
            source='student.person.full_name'
        )

        class Meta:
            """
            Meta class for Serializer
            """

            model = swapper.load_model('student_biodata', class_name)
            exclude = ('datetime_created','datetime_modified',)

    return Serializer


for key in serializer_dict:
    serializer_dict[key] = return_serializer(key)
