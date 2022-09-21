from typing import Any


class MSAOperatorInitError(ValueError):
    def __init__(self, mapping: Any):
        message = "Missing mapping %s to construct operator." % mapping
        super(MSAOperatorInitError, self).__init__(message)


class MSAOperatorBase(object):

    mappings = ()
    #upper_limt = None
    #lower_limit = None

    def __init__(self, *args, **kwargs):
        mapping: Any = None
        try:
            for mapping in self.mappings:
                if len(kwargs) > 0:
                    setattr(self, mapping, kwargs.pop(mapping))
                else:
                    setattr(self, mapping, args[0])
        except KeyError:
            raise MSAOperatorInitError(mapping)

    @property
    def variables(self):
        return vars(self)

    def __eq__(self, other):
        for arg in vars(self).keys():
            if getattr(self, arg) != getattr(other, arg):
                return False

        return True
