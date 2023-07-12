class Render:

    @staticmethod
    def _to_status_list(model, to_each_shape: callable):
        result = []
        if 'items' not in model:
            return {"result": [to_each_shape(model)]}
        for item in model['items']:
            result.append(to_each_shape(item))
        return {"result": result}

    @staticmethod
    def to_no_content(model):
        return {"result": ['no content']}

    @staticmethod
    def to_raw_content(model):
        return {"result": model}
