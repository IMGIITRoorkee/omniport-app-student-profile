import swapper
from rest_framework import serializers
from kernel.models.generics.contact_information import ContactInformation

# This serializer will be used in Reference model

class ReferenceSerializer(serializers.ModelSerializer):
    """
    Serializer class for Reference model
    """
    student = serializers.ReadOnlyField(
        source='student.person.full_name'
    )
    class Meta:
        model = swapper.load_model('student_biodata','Reference')
        fields = '__all__'

class ContactInformationSerializer(serializers.ModelSerializer):
    """
    Serializer class for ContactInformation model
    """
    class Meta:
        model = ContactInformation
        fields = '__all__'

