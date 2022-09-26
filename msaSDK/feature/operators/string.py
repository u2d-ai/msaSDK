from msaSDK.feature.base import MSAOperatorBase
from msaSDK.feature.base.registry import operators


class EqualsStripIgnoreCase(MSAOperatorBase):

    name = "strip_ignorecase_equals"
    group = "string"
    preposition = "strip ignore case equal to"
    mappings = ("value",)

    def applies_to(self, mapping):
        mapping = str(mapping)

        return mapping.lower().strip() == self.value.lower().strip()

    def __str__(self):
        return '%s "%s"' % (self.preposition, self.value.lower())


operators.register(EqualsStripIgnoreCase)
