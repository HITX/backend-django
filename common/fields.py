from django.db import models
from decimal import Decimal

class CurrencyField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 8
        kwargs['decimal_places'] = 2
        super(CurrencyField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CurrencyField, self).deconstruct()
        del kwargs['max_digits']
        del kwargs['decimal_places']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return value.quantize(Decimal('0.01'))
        # return (
        #     super(CurrencyField, self)
        #     .from_db_value(value, expression, connection, context)
        #     .quantize(Decimal('0.01'))
        # )
