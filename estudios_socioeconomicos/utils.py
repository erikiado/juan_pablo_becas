

def save_foreign_relashionship(objects, serializer_class, foreign_key=None):
    """ Saves nested relashionships in serializer of objects that have a Foreign
        Key object that must be saved first.

        Parameters
        ----------
            objects : list
                A list with the data of the object to be created

            serializer_class: rest_framework.serializers.ModelSerializer
                A class to serialize the data into a model instance.

            foreign_key : django.db.models.Model
                A instance of an object that needs to be referenced.

        Returns
        --------
            created_objects : list
                A list of all instances created.


    """
    created_objects = []

    for obj in objects:
        obj_serializer = serializer_class(data=obj)

        if obj_serializer.is_valid():
            if foreign_key:
                created_objects.append(obj_serializer.create(foreign_key))
            else:
                created_objects.append(obj_serializer.create())

    return created_objects


def update_foreign_relashionsip(objects, serializer_class, model_class, validated_data):
    """ Updated nested relashionships in serializer of objects.

        Parameters
        ----------
        objects : list
            A list with the data of the object to be updated.

        serializer_class: rest_framework.serializers.ModelSerializer
            A class to serialize the data into a model instance.

        model_cass : django.db.models.Model
            The class of object that must be retrieved to update.

        validated_data : list
            A list with the validated data of the object to be updated.
            DRF validation removes IDS on validation.

        Returns
        --------
            created_objects : list
                A list of all instances updated.
    """
    updated_objects = []

    for obj_info, data in zip(objects, validated_data):
        instance = model_class.objects.get(pk=obj_info.get('id'))
        serializer = serializer_class(instance, data=data)

        if serializer.is_valid():
            updated_objects.append(serializer.update())

    return updated_objects
