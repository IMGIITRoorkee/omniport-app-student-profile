import swapper

from rest_framework import serializers

from student_profile.utils.get_decorated_degree import (
    get_decorated_degree_with_graduation
)


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
    branch = serializers.ReadOnlyField(
        source='student.branch.name'
    )
    current_cgpa = serializers.SerializerMethodField()
    degree_sem = serializers.SerializerMethodField()
    email_address = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for Profile
        """

        model = swapper.load_model('student_biodata', 'Profile')
        exclude = ('datetime_created', 'datetime_modified')

    def get_current_cgpa(self, instance):
        return instance.student.current_cgpa if instance.show_cgpa else None

    def get_degree_sem(self, instance):
        return get_decorated_degree_with_graduation(instance.student)

    def get_email_address(self, instance):
        try:
            contact_info = instance.student.person.contact_information.get()
            return contact_info.institute_webmail_address
        except:
            return None
