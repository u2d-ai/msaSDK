from collections import defaultdict

from msaSDK.feature.base.settings import MSAFeatureSettings, get_msa_feature_settings

def all_false_if_empty(iterable):
    if not iterable:
        return False

    for element in iterable:
        if not element:
            return False
    return True

class MSAConditionsDict(defaultdict):

    @classmethod
    def from_conditions_list(cls, conditions):
        conditions_dict = cls(set)

        for cond in conditions:
            conditions_dict[cond.argument.COMPATIBLE_TYPE].add(cond)

        return conditions_dict

    def get_by_input(self, inpt):
        return self.get_by_type(type(inpt))

    def get_by_type(self, to_get_key):
        if to_get_key in self:
            return self[to_get_key]
        for key_type in self:
            if issubclass(to_get_key, key_type):
                return self[key_type]

        # raise the correct exception
        return self[to_get_key]


class MSACondition(object):

    """
    A Condition is the configuration of an argument, its attribute and an
    operator. It tells you if it itself is true or false given an input.
    The ``argument`` defines what this condition is checking.  Perhaps it's a
    ``User`` or ``Request`` object. The ``attribute`` name is then extracted out
    of an instance of the argument to produce a variable. That variable is then
    compared to the operator to determine if the condition applies to the input
    or not.
    For example, for the request IP address, you would define a ``Request``
    argument, that had an ``ip`` property.  A condition would then be constructed
    like so:
    from myapp.gutter import RequestArgument
    from gutter.client.models import Condition
        >> condition = Condition(argument=RequestArgument, attribute='ip', operator=some_operator)
    When the Condition is called, it is passed the input. The argument is then
    called (constructed) with input object to produce an instance.  The
    attribute is then extracted from that instance to produce the variable.
    The extracted variable is then checked against the operator.
    To put it another way, say you wanted a condition to only allow your switch
    to people between 15 and 30 years old.  To make the condition:
        1. You would create a ``UserArgument`` class that takes a user object in
           its constructor.  The class also has an ``age`` method which returns
           the user object's age.
        2. You would then create a new Condition via:
           ``Condition(argument=UserInput, attribute='age', operator=Between(15, 30))``.
        3. You then call that condition with a ``User``, and it would return
           ``True`` if the age of the user the ``UserArgument`` instance wraps
           is between 15 and 30.
    """

    def __init__(self, argument, attribute, operator, negative=False,
            settings:MSAFeatureSettings = get_msa_feature_settings()):
        self.attribute = attribute
        self.argument = argument
        self.operator = operator
        self.negative = negative
        self.settings = settings

    @property
    def __is_or_is_not(self):
        return 'is not' if self.negative else 'is'

    def __repr__(self):
        argument = ".".join((self.argument.__name__, self.attribute))
        return '<Condition "%s" %s %s>' % (argument, self.__is_or_is_not, self.operator)

    def __str__(self):
        return "%s %s %s" % (self.argument_string, self.__is_or_is_not, self.operator)

    def __eq__(self, other):
        return (
            self.argument == other.argument and
            self.attribute == other.attribute and
            self.operator == other.operator and
            self.negative is other.negative
        )

    def call(self, inpt):
        """
        Returns if the condition applies to the ``inpt``.
        If the class ``inpt`` is an instance of is not the same class as the
        condition's own ``argument``, then ``False`` is returned.  This also
        applies to the ``NONE`` input.
        Otherwise, ``argument`` is called, with ``inpt`` as the instance and
        the value is compared to the ``operator`` and the Value is returned.  If
        the condition is ``negative``, then then ``not`` the value is returned.
        Keyword Arguments:
        inpt -- An instance of the ``Input`` class.
        """
        if inpt is Manager.NONE_INPUT:
            return False

        # Call (construct) the argument with the input object
        argument_instance = self.argument(inpt)

        if not argument_instance.applies:
            return False

        application = self.__apply(argument_instance, inpt)

        if self.negative:
            application = not application

        return application

    @property
    def argument_string(self):
        parts = [self.argument.__name__, self.attribute]
        return '.'.join(map(str, parts))

    def __apply(self, argument_instance, inpt):
        variable = getattr(argument_instance, self.attribute)

        try:
            return self.operator.applies_to(variable)
        except Exception as error:
            signals.condition_apply_error.call(self, inpt, error)
            return False
