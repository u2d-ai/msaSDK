from msaSDK.feature.base.operator import MSAOperatorBase
from msaSDK.feature.base.registry import operators

class Truth(MSAOperatorBase):

    name = 'true'
    group = 'identity'
    preposition = 'true'

    def applies_to(self, argument):
        return bool(argument)

    def __str__(self):
        return 'true'


operators.register(Truth)