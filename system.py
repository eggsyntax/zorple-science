"""Sets up the system and applies operations"""

import numpy as np
import random

from dataclasses import dataclass
from pprint import pprint

possible_classes = ["Blimbit", "Zorple", "Quibnix", "Snarflux", "Drazzle", "Frobnak", "Wizzit", "Glompus", "Flubbert", "Snigglet",]
possible_adjectives = ["Fligglarious", "Quandrizzy", "Zibblastic", "Dofflepuff", "Fribbly", "Glarptastic", "Sprockleful", "Quizzleplex", "Blorficious", "Snoodly",]
possible_verbs = ["Splorficates", "Zizzles", "Quonkifies", "Plimbers", "Bliffles", "Wuzzles", "Frumbers", "Snibbles", "Dradzles", "Quindles",]
possible_variables = ["Quiffinity", "Snorptitude", "Blivviosity", "Snibbleness", "Drazzleplex", "Flibbitude", "Quonkensity", "Splorbalism", "Glumbracity", "Zibblosity",]

# TODO adopt a convention where k_foo refers to the type foo, and n_foo refers to instances of foo
n_classes = 1
n_adjectives = 3
n_ops = 2
n_constraints = 0
n_vars = 2

n_objects = 5

def create_variable(name):
    props = {}
    props['type'] = 'variable'
    props['name'] = name
    props['mean'] = (1 - np.random.power(5)) * 100 - 50
    relative_std_dev = np.random.uniform(0.0, 2.0)
    props['sdev'] = abs(props['mean'] * relative_std_dev)
    # props['adjective_list'] = random.sample(possible_adjectives, n_adjectives)
    # props['verb_list'] = random.sample(possible_verbs, n_ops)
    # props['variable_list'] = random.sample(possible_variables, n_vars)
    return props

def create_var_value(variable):
    value = np.random.normal(variable['mean'], variable['sdev'])
    # print(f'{variable["name"]} value ({variable["mean"]}, {variable["sdev"]}: {value}')
    return value

def create_class(name):
    props = {}
    props['type'] = 'class'
    props['name'] = name
    props['adjective_list'] = random.sample(possible_adjectives, n_adjectives)
    props['variable_list'] = [create_variable(name) for name in random.sample(possible_variables, n_vars)]
    return props

def create_object(clazz):
    obj = {}
    obj['type'] = 'object'
    obj['class'] = clazz
    obj['variables'] = {var['name']: create_var_value(var)  for var in clazz['variable_list']}
    return obj

def setup_system():
    system = {}
    system['classes'] = [create_class(name) for name in random.sample(possible_classes, n_classes)]
    system['objects'] = [create_object(random.choice(system['classes'])) for _ in range(n_objects)]
    return system







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
