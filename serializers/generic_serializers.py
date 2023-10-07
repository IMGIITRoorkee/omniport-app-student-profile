import swapper

from rest_framework import serializers

# Common Dictionary storing serializers and viewsets of similar models

common_dict = {
    'Interest': {'serializer': None, 'viewset': None},
    'Achievement': {'serializer': None, 'viewset': None},
    'CurrentEducation': {'serializer': None, 'viewset': None},
    'PreviousEducation': {'serializer': None, 'viewset': None},
    'Position': {'serializer': None, 'viewset': None},
    'Experience': {'serializer': None, 'viewset': None},
    'Project': {'serializer': None, 'viewset': None},
    'Book': {'serializer': None, 'viewset': None},
    'Paper': {'serializer': None, 'viewset': None},
    'Referee': {'serializer': None, 'viewset': None},
    'Skill': {'serializer': None, 'viewset': None},
}

models = {}
for key in common_dict.keys():
    models[key] = swapper.load_model('student_biodata', key)


def return_serializer(class_name):
    """
    Return the serializer for the given class
    :param class_name: the class whose serializer is being generated
    """

    class Serializer(serializers.ModelSerializer):
        """
        Serializer class for given class name
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if class_name == "PreviousEducation":
                self.fields['graduation_display'] = serializers.ReadOnlyField(
                    source='get_graduation_display')

        student = serializers.ReadOnlyField(
            source='student.person.full_name'
        )

        def create(self, validated_data):

            # For previous education
            # If percentage not specified, set is_percentage as False
            # Else use original value
            if class_name == 'PreviousEducation':
                cgpa = validated_data.get('cgpa', None)
                percentage = validated_data.get('percentage', None)
                # cgpa exists, percentage doesn't exist
                if percentage is None and cgpa is not None:
                    validated_data['is_percentage'] = False
                # percentage exists, cgpa doesn't exist
                elif cgpa is None and percentage is not None:
                    validated_data['is_percentage'] = True
                # both exists
                elif cgpa is not None and percentage is not None:
                    pass
                # both doesn't exists
                else:
                    raise serializers.ValidationError({
                        'Error': [
                            'Both CGPA and Percentage cannot be blank '
                            'simultaneously.'
                        ]
                    })

            # For allowing unverification of entity by students
            # and allowing change in description only if verified already
            verified = validated_data.get('verified', None)
            if verified is True:
                validated_data.pop('verified')

            return super().create(validated_data)

        def update(self, instance, validated_data):

            # For previous education
            # Same as done in create method
            if instance.__class__.__name__ == "PreviousEducation":
                cgpa = validated_data.get('cgpa', instance.cgpa)
                is_percentage = validated_data.get(
                    'is_percentage', instance.is_percentage)
                percentage = validated_data.get(
                    'percentage', instance.percentage)
                # cgpa exists, percentage doesn't exists
                if percentage is None and cgpa is not None:
                    instance.is_percentage = False
                # percentage exists, cgpa doesn't exist
                elif cgpa is None and percentage is not None:
                    instance.is_percentage = True
                # both exists
                elif cgpa is not None and percentage is not None:
                    instance.is_percentage = is_percentage
                else:
                    raise serializers.ValidationError({
                        'Error': [
                            'Both CGPA and Percentage cannot be blank '
                            'simultaneously.'
                        ]
                    })

            # For allowing unverification of entity by students
            verified = getattr(instance, 'verified', False)

            if verified is True:
                # For allowing change in project and experience description, even after verification
                if instance.__class__.__name__ != "Position" and hasattr(instance, 'description'):
                    instance.description = validated_data.get(
                        'description', instance.description
                    )
                    
                new_visibility = validated_data.get(
                    'visibility', instance.visibility
                )
                new_verified = validated_data.get(
                    'verified', instance.verified
                )
                instance.visibility = new_visibility
                instance.verified = new_verified
                instance.save()
                return instance
            else:
                new_verified = validated_data.get('verified', False)
                if new_verified is True:
                    validated_data.pop('verified')
                return super().update(instance, validated_data)

        class Meta:
            """
            Meta class for Serializer
            """

            model = models[class_name]
            exclude = ('datetime_created', 'datetime_modified',)

    return Serializer


for key in common_dict:
    common_dict[key]["serializer"] = return_serializer(key)
