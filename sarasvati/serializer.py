class Serializer:
    def __init__(self):
        self.__options = {}

    def register(self, name, serializer):
        self.__options[name] = serializer

    def serialize(self, model):
        result = {}
        for component in model.components:
            serializer = self.__serializer(component.name)

            if not serializer:
                raise Exception("No serializer found for '{}'".format(component.name))

            data = serializer.serialize(component)
            if data:
                result[component.name] = data
        return result

    def deserialize(self, model, data):
        for key in data.keys():
            component_data = data[key]
            serializer = self.__serializer(key)
            if not serializer:
                raise Exception("No serializer found for '{}'".format(key))

            if model.has_component(key):
                component = model.get_component(key)
                serializer.deserialize(component_data, component)
            else:  # create new component if not exist
                component = serializer.deserialize(component_data)
                model.add_component(component)

        return model

    def __serializer(self, name):
        return self.__options.get(name, None)
