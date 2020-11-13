import swapper
from rest_framework import serializers

from omniport.utils import switcher

Student = swapper.load_model('kernel', 'Student')
BaseSerializer = switcher.load_serializer('kernel', 'Student')


class StudentSearchSerializer(serializers.ModelSerializer):
    """
    Serializer that serializes the Student search query.
    """

    class Meta:
        model = Student

    def to_representation(self, obj):
        if isinstance(obj, Student):
            serializer = StudentSerializer(obj)
        else:
            raise Exception('No match found')
        return serializer.data


class StudentSerializer(BaseSerializer):
    """
    Serializer that serializes Student objects.
    """

    name = serializers.CharField(
        source='person.full_name',
        read_only=True,
    )
    display_picture = serializers.ImageField(
        source='person.display_picture',
        read_only=True,
    )

    handle = serializers.CharField(
        source='profile.handle',
        read_only=True,
        default=''
    )

    class Meta:
        model = Student

        fields = [
            'name',
            'display_picture',
            'handle',
            'enrolment_number',
        ]
