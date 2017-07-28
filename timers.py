from test_serializer import *
from itertools import chain
from functools import reduce
import timeit

num_items_per_model = 50

lots_o_meals = list(chain(
    [Breathatarian('eater{}'.format(x)) for x in range(0,num_items_per_model)],
    [Diet('eater{}'.format(x),'water') for x in range(num_items_per_model,num_items_per_model * 2)],
    [Snack('eater{}'.format(x),'water','candy') for x in range(num_items_per_model*2,num_items_per_model * 3)],
    [Meal('eater{}'.format(x),'water','chicken') for x in range(num_items_per_model * 3,num_items_per_model * 4)],
    [TastingMenu('eater{}'.format(x),'water','chicken','jello') for x in range(num_items_per_model * 4,num_items_per_model * 5)],
    ))

def loopy():
    fields = []
    for m in lots_o_meals:
        fields.extend(list(vars(m).keys()))
        fieldset = set(fields)


def crafty():
    def add_to_set(accumulated, item):
        accumulated[item.__class__.__name__] = item
        return accumulated

    unique_models = reduce(add_to_set,
                           lots_o_meals,
                           {})
    fieldset = list(
        chain(
            (list(vars(m).keys() for m in unique_models.values()))
        ))

print( "Results for {} models".format(num_items_per_model))
print( "Crafty: {}".format(timeit.timeit('crafty()', number=1000, globals=globals())) )
print( "Loopy:  {}".format(timeit.timeit('loopy()', number=1000, globals=globals())) )