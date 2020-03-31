class CustomObject:
    is_custom = True

    def __getitem__(self, item):
        attr = getattr(self, item)
        if hasattr(attr, 'is_custom'):
            return dict(attr)
        elif isinstance(attr, list):
            return array_return(attr)
        else:
            return attr


def array_return(attr: list):
    array = []
    for _item in attr:
        if hasattr(_item, 'is_custom'):
            array.append(dict(_item))
        elif isinstance(_item, list):
            array.append(array_return(_item))
        else:
            array.append(_item)
    return array
