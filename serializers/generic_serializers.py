import swapper

from rest_framework import serializers

# Common Dictionary storing serializers and viewsets of similar models 

common_dict = {
    'Profile': {'serializer': None,'viewset': None},
    'Interest': {'serializer': None,'viewset': None},
    'Achievement': {'serializer': None,'viewset': None},
    'CurrentEducation': {'serializer': None,'viewset': None},
    'PreviousEducation': {'serializer': None,'viewset': None},
    'Position': {'serializer': None,'viewset': None},
    'Experience': {'serializer': None,'viewset': None},
    'Project': {'serializer': None,'viewset': None},
    'Book': {'serializer': None,'viewset': None},
    'Paper': {'serializer': None,'viewset': None},
    'Referee': {'serializer': None,'viewset': None},
    'Skill': {'serializer': None,'viewset': None},
}

models = {}
for key in common_dict:
    models[key] = swapper.load_model('student_biodata', key)

def return_serializer(class_name):
    """
    Return the serializer for the given class
    :param class_name: the class whose serializer is being generated
    """

    if (class_name == "CurrentEducation" or class_name == "PreviousEducation"):

        class Serializer(serializers.ModelSerializer):
            """
            Serializer for given class name
            """
        
            student = serializers.ReadOnlyField(
                source='student.person.full_name'
            )

            verified = serializers.ReadOnlyField()

            class Meta:
                """
                Meta class for Serializer
                """

                model = models[class_name]
                exclude = ('datetime_created','datetime_modified',)

        return Serializer

    else:
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

                model = models[class_name]
                exclude = ('datetime_created','datetime_modified',)
        
        return Serializer

for key in common_dict:
    common_dict[key]["serializer"] = return_serializer(key)
