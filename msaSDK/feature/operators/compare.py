from msaSDK.feature.base.operator import MSAOperatorBase
from msaSDK.feature.base.registry import operators


class Equals(MSAOperatorBase):

    name = 'equals'
    group = 'comparable'
    preposition = 'equal to'
    mappings = ('value',)

    def applies_to(self, mapping):
        return mapping == self.value

    def __str__(self):
        return 'equal to "%s"' % self.value


class Between(MSAOperatorBase):

    name = 'between'
    group = 'comparable'
    preposition = 'between'
    mappings = ('lower_limit', 'upper_limit')

    def applies_to(self, mapping):
        return mapping > self.lower_limit and mapping < self.upper_limit

    def __str__(self):
        return 'between "%s" and "%s"' % (self.lower_limit, self.upper_limit)


class LessThan(MSAOperatorBase):

    name = 'before'
    group = 'comparable'
    preposition = 'less than'
    mappings = ('upper_limit',)

    def applies_to(self, mapping):
        return mapping < self.upper_limit

    def __str__(self):
        return 'less than "%s"' % self.upper_limit


class LessThanOrEqualTo(LessThan):

    name = 'less_than_or_equal_to'
    group = 'comparable'
    preposition = 'less than or equal to'

    def applies_to(self, mapping):
        return mapping <= self.upper_limit

    def __str__(self):
        return 'less than or equal to "%s"' % self.upper_limit


class MoreThan(MSAOperatorBase):

    name = 'more_than'
    group = 'comparable'
    preposition = 'more than'
    mappings = ('lower_limit',)

    def applies_to(self, mapping):
        return mapping > self.lower_limit

    def __str__(self):
        return 'more than "%s"' % self.lower_limit


class MoreThanOrEqualTo(MoreThan):

    name = 'more_than_or_equal_to'
    group = 'comparable'
    preposition = 'more than or equal to'

    def applies_to(self, mapping):
        return mapping >= self.lower_limit

    def __str__(self):
        return 'more than or equal to "%s"' % self.lower_limit


operators.register(Equals)
operators.register(Between)
operators.register(LessThan)
operators.register(LessThanOrEqualTo)
operators.register(MoreThan)
operators.register(MoreThanOrEqualTo)