
class MSASignal(object):

    def __init__(self):
        self.__callbacks = []

    def connect(self, callback):
        if not callable(callback):
            raise ValueError("Callback argument must be callable")

        self.__callbacks.append(callback)

    def call(self, *args, **kwargs):
        for callback in self.__callbacks:
            callback(*args, **kwargs)

    def reset(self):
        self.__callbacks = []


switch_registered = MSASignal()
switch_unregistered = MSASignal()
switch_updated = MSASignal()
condition_apply_error = MSASignal()
switch_checked = MSASignal()
switch_active = MSASignal()
