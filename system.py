"""Sets up the system and applies operations"""

import numpy as np
import operator as op
import random

from dataclasses import dataclass
from pprint import pprint

possible_classes = ["Blimbit", "Zorple", "Quibnix", "Snarflux", "Drazzle", "Frobnak", "Wizzit", "Glompus", "Flubbert", "Snigglet",]
possible_adjectives = ["Fligglarious", "Quandrizzy", "Zibblastic", "Dofflepuff", "Fribbly", "Glarptastic", "Sprockleful", "Quizzleplism", "Blorficious", "Snoodly",]
possible_verbs = ["Splorficates", "Zizzles", "Quonkifies", "Plimbers", "Bliffles", "Wuzzles", "Frumbers", "Snibbles", "Dradzles", "Quindles",]
possible_variables = ["Quiffinity", "Snorptitude", "Blivviosity", "Snibbleness", "Drazzleplism", "Flibbitude", "Quonkensity", "Splorbalism", "Glumbracity", "Zibblosity",]

operations = [op.add, op.sub, op.mul, op.truediv]

# TODO adopt a convention where k_foo refers to the type foo, and n_foo refers to instances of foo
n_classes = 1
n_adjectives = 3
n_ops = 2
n_constraints = 0
n_vars = 2

n_objects = 5

random.seed(10) # for reproducibility
rng = np.random.default_rng(10)

def create_variable(name):
    props = {}
    props['type'] = 'variable'
    props['name'] = name
    props['mean'] = (1 - rng.power(5)) * 100 - 50
    relative_std_dev = rng.uniform(0.0, 2.0)
    props['sdev'] = abs(props['mean'] * relative_std_dev)
    # props['adjective_list'] = random.sample(possible_adjectives, n_adjectives)
    # props['verb_list'] = random.sample(possible_verbs, n_ops)
    # props['variable_list'] = random.sample(possible_variables, n_vars)
    return props

def create_var_value(variable):
    value = rng.normal(variable['mean'], variable['sdev'])
    # print(f'{variable["name"]} value ({variable["mean"]}, {variable["sdev"]}: {value}')
    return value

def create_class(name):
    props = {}
    props['type'] = 'class'
    props['name'] = name
    props['adjective_list'] = random.sample(possible_adjectives, n_adjectives)
    props['variable_list'] = [create_variable(name) for name in random.sample(possible_variables, n_vars)]
    return props

def create_operation(variable, name):
    print(f'Variable in create_operation: {variable}') # XXX
    props = {}
    props['type'] = 'operation'
    props['name'] = name
    props['op'] = random.choice(operations)
    # TODO hmm, actually operand should just be 1 to n, and then the stdev should depend on the class it's being applied to
    # if * / truediv, then just multiply by operand; if + / -, then add/subtract (operand * stdev-of-class)
    props['first_operand'] = variable
    props['second_operand'] = rng.integers(0, 10)
    return props

def apply_operation(obj, op):
    f = op['op']
    old_value = obj['variables'][op['first_operand']['name']]
    # TODO if op is + or -, then multiply second_operand by stdev of class
    new_value = f(old_value, op['second_operand'])
    print(f'Applying operation {f} to {old_value} with {op["second_operand"]}, result: {new_value}')
    obj['variables'][op['first_operand']['name']] = new_value

def create_object(clazz):
    obj = {}
    obj['type'] = 'object'
    obj['class'] = clazz
    obj['variables'] = {var['name']: create_var_value(var)  for var in clazz['variable_list']}
    obj['adjectives'] = [adjective for adjective in clazz['adjective_list'] if rng.random() < 0.5]
    return obj

def run_initial_operations(system):
    pass

def some_objects(system, n=5): # XXX
    return[create_object(system['classes'][0]) for _ in range(n)]

def random_variable(classes):
    clazz = random.choice(classes)
    vars = clazz['variable_list']
    print(f'Variables of class {clazz['name']}: {vars}')
    var = random.choice(vars)
    print(f'Random variable: {var}')
    return var

def setup_system():
    system = {}
    classes = [create_class(name) for name in random.sample(possible_classes, n_classes)]
    system['classes'] = classes
    system['objects'] = [create_object(random.choice(system['classes'])) for _ in range(n_objects)]
    system['ops'] =     [create_operation(random_variable(classes), name) for name in random.sample(possible_verbs, n_ops)]
    system['history'] = [] # list of operations applied to objects
    return system

import code; code.interact(local=locals())

def spelling():
    # Spelling:
    #  LocalWords:  Blimbit Zorple Quibnix Snarflux Drazzle Frobnak Wizzit Glompus
    #  LocalWords:  Flubbert Snigglet Fligglorious Quandrizzy Zibblastic Dofflepuff
    #  LocalWords:  Fribbly Glarptastic Sprockleful Quizzleplex Blorficious Snoodly
    #  LocalWords:  Splorficates Zizzles Quonkifies Plimbers Bliffles Wuzzles
    #  LocalWords:  Frumbers Snibbles Dradzles Quindles Quiffinity Snorptitude
    #  LocalWords:  blimbit zorple quibnix snarflux drazzle frobnak wizzit glompus
    #  LocalWords:  Blivviosity Zapplemetrics Drazzleplex Flibbitude Quonkensity
    #  LocalWords:  Splorbalism Glumbracity Zibblenumber Zapplemetric Zibblosity
    #  localwords:  flubbert snigglet fligglorious quandrizzy zibblastic dofflepuff
    #  localwords:  fribbly glarptastic sprockleful quizzleplex blorficious snoodly
    #  localwords:  splorficates zizzles quonkifies plimbers bliffles wuzzles
    #  localwords:  frumbers snibbles dradzles quindles
    #  LocalWords:  blivviosity zapplemetrics drazzleplex flibbitude quonkensity
    #  LocalWords:  Snibbleness snibbleness zapplemetrics quonkensity zibblenumber
    #  LocalWords:  glumbracity Fligglarious
    #  localwords:  splorbalism zibblenumber
    pass
