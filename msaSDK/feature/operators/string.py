from msaSDK.feature.base import MSAOperatorBase
from msaSDK.feature.base.registry import operators
from msaSDK.feature.mapping.variables import MSAVariableBase


class EqualsStripIgnoreCase(MSAOperatorBase):

    name = 'strip_ignorecase_equals'
    group = 'string'
    preposition = 'strip ignore case equal to'
    arguments = ('value',)

    def applies_to(self, argument):
        if isinstance(argument, MSAVariableBase):
            argument = str(argument.value)
        else:
            argument = str(argument)

        return argument.lower().strip() == self.value.lower().strip()

    def __str__(self):
        return '%s "%s"' % (self.preposition, self.value.lower())

operators.register(EqualsStripIgnoreCase)