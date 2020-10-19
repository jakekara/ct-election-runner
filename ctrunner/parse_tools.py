"""Helper functions for parser.py 

Keeping functions in here that should not be called from ctrunner client code.
"""


def unwrap_object(obj, force_key=None):
    """
    'Unwrap' this weird format a lot of this data is in, where there's
    an object containing one key, with a value that is the actual object
    you want. The key is usually the same as an ID field in the inner object
    """
    keys = obj.keys()
    assert len(list(keys)) == 1, "Wrapped object must only have one key"
    obj_key = list(keys)[0]

    inner_obj = obj[obj_key]
    if inner_obj["ID"] == obj_key:
        return inner_obj
    else:
        if force_key:
            inner_obj[force_key] = obj_key
            return inner_obj
        raise Exception("Inner object has no ID field:\n" + json.dumps(obj, indent=2))
