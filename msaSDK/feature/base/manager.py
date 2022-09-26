import threading

from msaSDK.feature.base import signal
from msaSDK.feature.base.signal import switch_unregistered, switch_updated
from msaSDK.feature.base.switch import MSASwitch


class MSAManager(threading.local):
    """
    The Manager holds all state for msaSDK.features.  It knows what Switches have been
    registered, and also what Input objects are currently being applied.  It
    also offers an ``active`` method to ask it if a given switch name is
    active, given its conditions and current inputs.
    """

    #: Special singleton used to represent a "no input" which mappings can look
    #: for and ignore
    NONE_INPUT = object()

    def __init__(
            self,
            switch_class=MSASwitch,
            namespace=None,
            settings=None,
    ):
        self.settings = settings
        self.key_separator = self.settings.hirachy_seperator
        self.namespace_separator = self.settings.namespace_separator
        self.default_namespace = self.settings.default_namespace
        self.storage = self.settings.storage_engine
        self.autocreate = self.settings.autocreate
        self.inputs = self.settings.inputs

        if self.storage is None:
            # todo: make a better check
            raise TypeError("storage must be a dict like value")

        if self.inputs is None:
            self.inputs = []

        if namespace is None:
            namespace = self.default_namespace
        elif isinstance(namespace, str):
            namespace = [namespace]

        self.switch_class = switch_class
        self.namespace = namespace

    def __getstate__(self):
        inner_dict = vars(self).copy()
        inner_dict.pop("inputs", False)
        inner_dict.pop("storage", False)
        return inner_dict

    def __getitem__(self, key):
        return self.switch(key)

    def __contains__(self, key):
        return self.__namespaced(key) in self.storage

    def __delitem__(self, key):
        del self.storage[self.__namespaced(key)]

    @property
    def switches(self):
        """
        List of all switches currently registered.
        """
        results = [
            switch
            for name, switch in self.storage.iteritems()
            if name.startswith(self.__joined_namespace)
        ]

        return results

    def switch(self, name):
        """
        Returns the switch with the provided ``name``.
        If ``autocreate`` is set to ``True`` and no switch with that name
        exists, a ``DISABLED`` switch will be with that name.
        Keyword Mappings:
        name -- A name of a switch.
        """
        try:
            switch = self.storage[self.__namespaced(name)]
        except KeyError:
            if not self.autocreate:
                raise ValueError(
                    "No switch named '%s' registered in '%s'" % (name, self.namespace)
                )

            switch = self.__create_and_register_disabled_switch(name)

        switch.manager = self
        return switch

    def get_children(self, parent):
        namespaced_parent = self.__namespaced(parent) + ":"
        return [
            self.__denamespaced(child)
            for child in self.storage.keys()
            if child.startswith(namespaced_parent)
        ]

    def register(self, switch, signal=signal.switch_registered):
        """
        Register a switch and persist it to the storage.
        """
        if not switch.name:
            raise ValueError("MSASwitch name cannot be blank")

        switch.manager = None  # Prevents having to serialize the manager
        self.__sync_parental_relationships(switch)
        self.__persist(switch)
        switch.manager = self
        signal.call(switch)

    def unregister(self, switch_or_name):
        name = getattr(switch_or_name, 'name', switch_or_name)
        switch = self.switch(name)

        map(self.unregister, switch.children)

        del self.storage[self.__namespaced(name)]
        switch_unregistered.call(switch)

    def input(self, *inputs):
        self.inputs = list(inputs)

    def flush(self):
        self.inputs = []

    def active(self, name, *inputs, **kwargs):
        switch = self.switch(name)

        if not kwargs.get("exclusive", False):
            inputs = tuple(self.inputs) + inputs

        # Also check the switches against "NONE" input. This ensures there will
        # be at least one input checked.
        if not inputs:
            inputs = (self.NONE_INPUT,)

        # If necessary, the switch first consents with its parent and returns
        # false if the switch is consenting and the parent is not enabled for
        # ``inputs``.

        if (switch.concent and switch.parent and
                not self.active(switch.parent.name, *inputs, **kwargs)):
            return False

        return any(map(switch.enabled_for, inputs))

    def update(self, switch):

        self.register(switch, signal=switch_updated)

        if switch.changes.get('name'):
            old_name = switch.changes['name'].get('previous')
            del self.storage[self.__namespaced(old_name)]

        switch.reset()

        # If this switch has any children, it's likely their instance of this
        # switch (their ``parent``) is now "stale" since this switch has
        # been updated. In order for them to pick up their new parent, we need
        # to re-save them.
        #
        # ``register`` is not used here since we do not need/want to sync
        # parental relationships.
        for child in getattr(switch, 'children', []):
            self.__persist(child)

    def namespaced(self, namespace):
        new_namespace = []

        # Only start with the current namesapce if it's not the default
        # namespace
        if self.namespace is not self.default_namespace:
            new_namespace = list(self.namespace)

        new_namespace.append(namespace)

        return type(self)(
            storage=self.storage,
            autocreate=self.autocreate,
            inputs=self.inputs,
            switch_class=self.switch_class,
            namespace=new_namespace,
        )

    def __persist(self, switch):
        self.storage[self.__namespaced(switch.name)] = switch
        return switch

    def __create_and_register_disabled_switch(self, name):
        switch = self.switch_class(name)
        switch.state = self.switch_class.states.DISABLED
        self.register(switch)
        return switch

    def __sync_parental_relationships(self, switch):
        try:
            parent_key = self.__parent_key_for(switch)
            new_parent = self.switch(parent_key)
        except ValueError:
            new_parent = None

        old_parent = switch.parent

        switch.parent = new_parent

        if old_parent and old_parent is not new_parent:
            old_parent.children.remove(switch)
            old_parent.save()

        if new_parent:
            new_parent.children.append(switch)
            new_parent.save()

    def __parent_key_for(self, switch):
        # TODO: Make this a method on the switch object
        # return self.name.rsplit(self.key_separator, 1)[:-1]
        parent_parts = switch.name.split(self.key_separator)[:-1]
        return self.key_separator.join(parent_parts)

    def __namespaced(self, name=""):
        if not self.__joined_namespace:
            return name
        else:
            return self.namespace_separator.join((self.__joined_namespace, name))

    def __denamespaced(self, name=""):
        prefix = self.__joined_namespace + self.namespace_separator
        if prefix and name.startswith(prefix):
            return name.replace(prefix, "", 1)
        return name

    @property
    def __joined_namespace(self):
        return self.namespace_separator.join(self.namespace)
