import swapper

from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for Profile
    """

    student = serializers.ReadOnlyField(
        source='student.person.full_name'
    )
    enrolment_number = serializers.IntegerField(
        source='student.enrolment_number',
        read_only=True
    )

    class Meta:
        """
        Meta class for Profile
        """

        model = swapper.load_model('student_biodata', 'Profile')
        exclude = ('datetime_created', 'datetime_modified')
