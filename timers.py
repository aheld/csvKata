import timeit
from itertools import chain
from functools import reduce
from collections import OrderedDict
from test_serializer import Breathatarian, Diet, Snack, Meal, TastingMenu


EXPECTED = {'beverage', 'protein', 'dessert', 'eater'}


def get_models(num):
    return list(chain(
        [Breathatarian('eater{}'.format(x))
            for x in range(0, num)],
        [Diet('eater{}'.format(x), 'water')
            for x in range(num, num * 2)],
        [Snack('eater{}'.format(x), 'water', 'candy')
            for x in range(num*2, num * 3)],
        [Meal('eater{}'.format(x), 'water', 'chicken')
            for x in range(num * 3, num * 4)],
        [TastingMenu('eater{}'.format(x), 'water', 'chicken', 'jello')
            for x in range(num * 4, num * 5)],
        ))


def try_looper(meals):
    '''Simple loop construct,
        build all the fields and then make a set'''
    fields = []
    for m in meals:
        fields.extend(list(vars(m).keys()))
        fieldset = set(fields)
    assert EXPECTED == fieldset


def try_list_comp_basic(meals):
    def get_next_prop():
        for props in [vars(m).keys() for m in meals]:
            for prop in props:
                yield prop
    list_of_props = [x for x in get_next_prop()]
    fieldset = set(list_of_props)
    assert EXPECTED == fieldset


def try_list_comp_lists(meals):
    list_of_props = [vars(m).keys() for m in meals]
    all_the_props = list(chain.from_iterable(list_of_props))
    fieldset = set(all_the_props)
    assert EXPECTED == fieldset


def try_list_comp_gen(meals):
    list_of_props = [vars(m).keys() for m in meals]
    all_the_props = chain.from_iterable(list_of_props)
    fieldset = set(all_the_props)
    assert EXPECTED == fieldset


def try_set_comp_simple(meals):
    list_of_props = {frozenset(vars(m).keys()) for m in meals}
    all_the_props = chain.from_iterable(list_of_props)
    fieldset = set(all_the_props)
    assert EXPECTED == fieldset


def try_functional(meals):
    def add_to_set(accumulated, item):
        accumulated[item.__class__.__name__] = item
        return accumulated

    unique_models = reduce(add_to_set,
                           meals,
                           {})
    fieldset = set(
        chain.from_iterable(
            (vars(m).keys() for m in unique_models.values())
        ))
    assert EXPECTED == fieldset


def run_and_time(func_name, num):
    return timeit.timeit('{}(get_models({}))'.format(func_name, num),
                         number=10,
                         globals=globals())


def report(runs, num):
    fastest = min(runs.values())
    print("Results for {} models".format(num))
    print("{}{}{}".format("  function".ljust(24),
                          "time".ljust(11), "relative"))

    SORTED_RUNS = OrderedDict(sorted(runs.items(), key=lambda t: t[1]))

    for func_name, timed_run in SORTED_RUNS.items():
        if timed_run == fastest:
            label = ' Baseline'
        else:
            label = ' times longer'
        print(" {} {:08.6f}  {:6.2f} {}".format(
            func_name.ljust(20), timed_run, (timed_run/fastest), label))


for num in [10, 100, 1000, 10000]:
    runs = {func_name: run_and_time(func_name, num)
            for func_name in locals() if func_name.startswith('try_')}
    report(runs, num)
