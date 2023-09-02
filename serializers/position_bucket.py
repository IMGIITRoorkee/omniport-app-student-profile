import swapper

from rest_framework import serializers

from student_profile.serializers.generic_serializers import return_serializer


class PositionBucketSerializer(serializers.ModelSerializer):
    '''
    Serializer class for PositionBucket model
    '''

    position = return_serializer('Position')

    class Meta:
        model = swapper.load_model('student_biodata', 'PositionBucket')
        exclude = ['datetime_created', 'datetime_modified']

class PositionBucketSlimSerializer(serializers.ModelSerializer):
    '''
    Serializer class for PositionBucket model
    '''

    class Meta:
        model = swapper.load_model('student_biodata', 'PositionBucket')
        exclude = ['datetime_created', 'datetime_modified']