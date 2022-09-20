from typing import Any


class MSAOperatorInitError(ValueError):

    def __init__(self, argument: Any):
        message = "Missing argument %s to construct operator." % argument
        super(MSAOperatorInitError, self).__init__(message)


class MSAOperatorBase(object):

    arguments = ()

    def __init__(self, *args, **kwargs):
        argument: Any = None
        try:
            for argument in self.arguments:
                setattr(self, argument, kwargs.pop(argument))
        except KeyError:
            raise MSAOperatorInitError(argument)

    @property
    def variables(self):
        return vars(self)

    def __eq__(self, other):
        for arg in vars(self).keys():
            if getattr(self, arg) != getattr(other, arg):
                return False

        return True