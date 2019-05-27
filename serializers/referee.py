import swapper
from rest_framework import serializers

from formula_one.models.generics.contact_information import ContactInformation

# This serializer will be used in Reference model

class ContactInformationSerializer(serializers.ModelSerializer):
    """
    Serializer class for ContactInformation model
    """
    class Meta:
        model = ContactInformation
        fields = ('primary_phone_number', 'secondary_phone_number', 'email_address', 'email_address_verified', 'institute_webmail_address', )


class RefereeSerializer(serializers.ModelSerializer):
    """
    Serializer class for Referee model
    """
    contact_information = ContactInformationSerializer(many=True,required=False)
    student = serializers.ReadOnlyField(
        source='student.person.full_name'
    )
    class Meta:
        model = swapper.load_model('student_biodata','Referee')
        fields = '__all__'



