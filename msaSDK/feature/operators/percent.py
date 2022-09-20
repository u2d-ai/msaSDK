from decimal import Context as decimal_Context, Decimal, DecimalException

from msaSDK.feature.base import MSAOperatorBase
from msaSDK.feature.base.registry import operators


class MSAPercentRange(MSAOperatorBase):

    name = 'percent_range'
    group = 'misc'
    preposition = 'in the percentage range of'
    mappings = ('lower_limit', 'upper_limit')

    _context = decimal_Context()

    def _modulo(self, decimal_mapping):
        """
        The mod operator is prone to floating point errors, so use decimal.
        101.1 % 100
        >>> 1.0999999999999943
        decimal_context.divmod(Decimal('100.1'), 100)
        >>> (Decimal('1'), Decimal('0.1'))
        """
        _times, remainder = self._context.divmod(decimal_mapping, 100)

        # match the builtin % behavior by adding the N to the result if negative
        return remainder if remainder >= 0 else remainder + 100

    def __init__(self, lower_limit, upper_limit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.upper_limit = self._context.create_decimal(str(upper_limit))
        self.lower_limit = self._context.create_decimal(str(lower_limit))

    def applies_to(self, mapping):
        try:
            decimal_mapping = Decimal(str(mapping))
        except DecimalException:
            decimal_mapping = Decimal(hash(mapping))

        return self.lower_limit <= self._modulo(decimal_mapping) < self.upper_limit

    def __str__(self):
        return 'in %0.1f - %0.1f%% of values' % (self.lower_limit, self.upper_limit)


class MSAPercent(MSAPercentRange):

    name = 'percent'
    group = 'misc'
    preposition = 'within the percentage of'
    mappings = ('percentage',)

    def __init__(self, percentage, lower_limit, upper_limit, *args, **kwargs):
        super().__init__(lower_limit, upper_limit, *args, **kwargs)
        self.upper_limit = float(percentage)
        self.lower_limit = 0.0

    @property
    def variables(self):
        return dict(percentage=self.upper_limit)

    def __str__(self):
        return 'in %s%% of values' % self.upper_limit


operators.register(MSAPercentRange)
operators.register(MSAPercent)