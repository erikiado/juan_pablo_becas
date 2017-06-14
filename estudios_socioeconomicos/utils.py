import os

def _delete_file(path):
   """ Deletes file from filesystem.
   Parameters:
   -----------
     path : A string that specify the location of the file.
   """
   if os.path.isfile(path):
       os.remove(path)

def save_foreign_relationship(objects, serializer_class, model_class, foreign_instance=None):
    """ Updated nested relashionships in serializer of objects.

        Saves or updates a nested serializer that has a Foreign Relashionship.

        Parameters
        -----------
        objects: []
            List of objects to save of update.

        serializer_class:
            from rest_framework import serializers.ModelSerializers class that
            creates or updates this object.

        model_class:
            django.db.models.Model class to which the objects belong to.

        foreign_instance:
            Serializer that creates this object might have am inverse Foreign
            relashionship an the object needs a reference to the instance.

        Returns
        --------
        List of created and updated objects.
    """
    if not objects:
        return

    updated_objects = []

    for obj in objects:

        if not obj:  # In case we get a None value (can't trust kids this days)
            break

        if obj.get('id'):  # Does the object exists?
            instance = model_class.objects.get(pk=obj.get('id'))
            serializer = serializer_class(instance, data=obj)

            if serializer.is_valid():
                updated_objects.append(serializer.update())  # Update

        else:
            serializer = serializer_class(data=obj)

            if serializer.is_valid():
                if not foreign_instance:
                    updated_objects.append(serializer.create())  # Create
                else:
                    updated_objects.append(serializer.create(foreign_instance))  # Create

    return updated_objects
