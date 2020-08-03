from functools import wraps, partial
from typing import List, NamedTuple, Set

from automated_logging.helpers import (
    Operation,
    get_or_create_thread,
    function2path,
)


def _normalize_view_args(methods: List[str]) -> Set[str]:
    if methods is not None:
        methods = {m.upper() for m in methods}

    return methods


def exclude_view(func=None, *, methods: List[str] = ()):
    """
    Decorator used for ignoring specific views, without adding them
    to the AUTOMATED_LOGGING configuration.

    This is done via the local threading object. This is done via the function
    name and module location.

    :param func: function to be decorated
    :param methods: methods to be ignored (case-insensitive),
                    None => No method will be ignored,
                    [] => All methods will be ignored

    :return: function
    """
    methods = _normalize_view_args(methods)

    if func is None:
        return partial(exclude_view, methods=methods)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ simple wrapper """
        thread, _ = get_or_create_thread()

        path = function2path(func)
        if (
            path in thread.dal['ignore.views']
            and thread.dal['ignore.views'][path] is not None
            and methods is not None
        ):
            methods.update(thread.dal['ignore.views'][path])

        thread.dal['ignore.views'][path] = methods

        return func(*args, **kwargs)

    return wrapper


def include_view(func=None, *, methods: List[str] = None):
    """
    Decorator used for including specific views **regardless** if they
    are included in one of the exclusion patterns, this can be selectively done
    via methods. Non matching methods will still go through the exclusion pattern
    matching.

    :param func: function to be decorated
    :param methods: methods to be included (case-insensitive)
                    None => All methods will be explicitly included
                    [] => No method will be explicitly included
    :return: function
    """
    methods = _normalize_view_args(methods)

    if func is None:
        return partial(include_view, methods=methods)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ simple wrapper """
        thread, _ = get_or_create_thread()

        path = function2path(func)
        if (
            path in thread.dal['include.views']
            and thread.dal['include.views'][path] is not None
            and methods is not None
        ):
            methods.update(thread.dal['include.views'][path])

        thread.dal['include.views'][path] = methods
        return func(*args, **kwargs)

    return wrapper


def _normalize_model_args(operations, fields) -> [Set[Operation], Set[str]]:
    if operations is not None:
        translation = {
            'create': Operation.CREATE,
            'modify': Operation.MODIFY,
            'delete': Operation.DELETE,
        }
        operations = {
            translation[o.lower()]
            for o in operations
            if o.lower() in translation.keys()
        }

    if fields is not None:
        fields = set(fields)

    return operations, fields


IgnoreModel = NamedTuple(
    "IgnoreModel", (('operations', Set[Operation]), ('fields', Set[str]))
)


def exclude_model(func=None, *, operations: List[str] = (), fields: List[str] = None):
    """
    Decorator used for ignoring specific models, without using the
    class or AUTOMATED_LOGGING configuration

    This is done via the local threading object. __module__ and __name__ are used
    to determine the right model.

    :param func: function to be decorated
    :param operations: operations to be ignored can be a list of:
                       modify, create, delete (case-insensitive)
                       [] => All operations will be ignored
                       None => No operation will be ignored
    :param fields: fields to be ignored in not ignored operations
                   [] => All fields will be ignored
                   None => No field will be ignored
    :return: function
    """
    operations, fields = _normalize_model_args(operations, fields)

    if func is None:
        return partial(exclude_model, operations=operations, fields=fields)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ simple wrapper """
        thread, _ = get_or_create_thread()
        path = function2path(func)

        if (
            path in thread['ignore.models']
            and thread['ignore.models'][path].operations is not None
            and operations is not None
        ):
            operations.update(thread['ignore.models'][path].operations)

        if (
            path in thread['ignore.models']
            and thread['ignore.models'][path].fields is not None
            and fields is not None
        ):
            fields.update(thread['ignore.models'][path].fields)

        thread.dal['ignore.models'][path] = IgnoreModel(operations, fields)

        return func(*args, **kwargs)

    return wrapper


IncludeModel = NamedTuple(
    "IncludeModel", (('operations', Set[Operation]), ('fields', Set[str]))
)


def include_model(func=None, *, operations: List[str] = (), fields: List[str] = None):
    """
    Decorator used for including specific models, despite potentially being ignored
    by the exclusion preferences set in the configuration.

    :param func: function to be decorated
    :param operations: operations to be ignored can be a list of:
                       modify, create, delete (case-insensitive)
                       [] => No operation will be explicitly included
                       None => All operations will be explicitly included
    :param fields: fields to be explicitly included
                   [] => No fields will be explicitly included
                   None => All fields will be explicitly included.

    :return: function
    """
    operations, fields = _normalize_model_args(operations, fields)

    if func is None:
        return partial(include_model, operations=operations, fields=fields)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ simple wrapper """
        thread, _ = get_or_create_thread()
        path = function2path(func)

        if (
            path in thread['include.models']
            and thread['include.models'][path].operations is not None
            and operations is not None
        ):
            operations.update(thread['include.models'][path].operations)

        if (
            path in thread['include.models']
            and thread['include.models'][path].fields is not None
            and fields is not None
        ):
            fields.update(thread['include.models'][path].fields)

        thread.dal['include.models'][path] = IncludeModel(operations, fields)

        return func(*args, **kwargs)

    return wrapper
