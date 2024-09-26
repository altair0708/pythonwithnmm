import warnings


def singleton(cls):
    warnings.warn('Deprecation method: singleton', DeprecationWarning)
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
