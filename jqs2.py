import datetime
from decimal import Decimal

import jsonpickle
import tushare

s_time = datetime.datetime.now()

print(datetime.datetime.now() - s_time)

val = Decimal(1.2)
print(str(val))
print(jsonpickle.dumps(123))
print(jsonpickle.loads('123'))

tushare.get_k_data('510900')
