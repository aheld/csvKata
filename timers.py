from test_serializer import *
from itertools import chain
from functools import reduce
import timeit

lots_o_meals = list(chain(
    [Breathatarian('eater{}'.format(x)) for x in range(0,100)],
    [Diet('eater{}'.format(x),'water') for x in range(100,200)],
    [Snack('eater{}'.format(x),'water','candy') for x in range(200,300)],
    [Meal('eater{}'.format(x),'water','chicken') for x in range(300,400)],
    [TastingMenu('eater{}'.format(x),'water','chicken','jello') for x in range(400,500)],
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

print( "Crafty: {}".format(timeit.timeit('crafty()', number=1000, globals=globals())) )
print( "loopy: {}".format(timeit.timeit('loopy()', number=1000, globals=globals())) )