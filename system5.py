"""Sets up the system and applies operations"""

import sys
import numpy as np
import operator as oper
import random
import uuid
import re

from dataclasses import dataclass
from pprint import pprint

# TODO replace nonsense names with generic name/number system.
possible_classes = ["blimbit", "zorple", "quibnix", "snarflux", "drazzle", "frobnak", "wizzit", "glompus", "flubbert", "snigglet",]
possible_adjectives = ["fligglarious", "quandrizzy", "zibblastic", "dofflepufous", "fribbly", "glarpastic", "sprocklish", "quizzleplistic", "blorficious", "snoodly",]
possible_verbs = ["splorficate", "zizzle", "quonkify", "plimber", "bliffle", "wuzzle", "frumber", "snibble", "dradzle", "quindle",]
possible_variables = ["quiffinity", "snorptitude", "blivviosity", "snibbleness", "drazzleplism", "flibbitude", "quonkensity", "splorbalism", "glumbracity", "zibblosity",]

# TODO I think we'll certainly want to add more operations at some point
operations = [oper.add, oper.sub, oper.mul, oper.truediv]

n_classes = 1
n_adjectives = 3
n_ops = 2
n_initial_ops = 3
n_constraints = 0
n_vars = 2

n_objects = 5

random.seed(10)  # for reproducibility
rng = np.random.default_rng(10)

def create_variable(name):
    props = {}
    props['type'] = 'variable'
    props['name'] = name
    props['mean'] = (1 - rng.power(5)) * 100 - 50
    relative_std_dev = rng.uniform(0.0, 2.0)
    props['sdev'] = abs(props['mean'] * relative_std_dev)
    return props

def create_var_value(variable):
    value = rng.normal(variable['mean'], variable['sdev'])
    return value

def create_class(name):
    props = {}
    props['type'] = 'class'
    props['name'] = name
    props['adjective_list'] = random.sample(possible_adjectives, n_adjectives)
    props['variable_list'] = [create_variable(name) for name in random.sample(possible_variables, n_vars)]
    return props

def create_operation(variable, name):
    props = {}
    props['type'] = 'operation'
    props['name'] = name
    props['op'] = random.choice(operations)
    # If * or /, then multiply by operand; if + or -, scale by the standard deviation.
    props['first_operand'] = variable
    props['second_operand'] = rng.integers(0, 10)
    return props

def apply_operation(system, obj, op):
    f = op['op']
    attr = op['first_operand']['name']
    old_value = obj['variables'][attr]
    operand2 = op['second_operand']
    if f in [oper.add, oper.sub]:
        operand2 *= op['first_operand']['sdev']
    new_value = f(old_value, operand2)
    print(f"\nApplying operation '{op['name']}' to attribute '{attr}':")
    print(f"  Old value: {old_value:.5g}")
    print(f"  Operand:   {operand2:.5g}")
    print(f"  New value: {new_value:.5g}\n")
    obj['variables'][attr] = new_value
    system['history'].append((op, obj, attr, new_value))
    # Update last changed attribute for the object.
    obj['last_changed'] = [(attr, new_value)]

def create_object(clazz):
    obj = {}
    obj['name'] = f'{clazz["name"]}{random.choice(range(1, 10000))}'
    obj['type'] = 'object'
    obj['class'] = clazz
    obj['variables'] = {var['name']: create_var_value(var) for var in clazz['variable_list']}
    obj['adjectives'] = [adjective for adjective in clazz['adjective_list'] if rng.random() < 0.5]
    obj['last_changed'] = []  # Initialize last_changed to empty list.
    return obj

def run_initial_operations(system, n):
    print('\nRunning initial operations:')
    objects = system['objects']
    ops = system['ops']
    for _ in range(n):
        obj = random.choice(objects)
        op = random.choice(ops)
        apply_operation(system, obj, op)
    print()

def print_object(obj):
    adjectives = obj['adjectives']
    adj_strings = [f"It is {adj}." for adj in adjectives]
    vars = obj['variables']
    varstrings = [f"Its {var} is {value:.5g}." for var, value in vars.items()]
    if obj['last_changed']:
        changes = obj['last_changed']
        if len(changes) == 1:
            change_str = f"Last changed: {changes[0][0]} = {changes[0][1]:.5g}"
        else:
            change_str = f"Last changed: {changes[0][0]} = {changes[0][1]:.5g} and others"
    else:
        change_str = "No recent changes."
    print(f"Object {obj['name']} is a {obj['class']['name']}.")
    print("  General properties: " + " ".join(adj_strings))
    print("  Values: " + " ".join(varstrings))
    print("  " + change_str)

def print_objects(system):
    for obj in system['objects']:
        print_object(obj)
        print()

def some_objects(system, n=5):
    return [create_object(system['classes'][0]) for _ in range(n)]

def random_variable(classes):
    clazz = random.choice(classes)
    vars = clazz['variable_list']
    var = random.choice(vars)
    return var

def setup_system(hidden_rule=None):
    system = {}
    classes = [create_class(name) for name in random.sample(possible_classes, n_classes)]
    system['classes'] = classes
    system['objects'] = [create_object(random.choice(system['classes'])) for _ in range(n_objects)]
    system['ops'] = [create_operation(random_variable(classes), name) for name in random.sample(possible_verbs, n_ops)]
    system['history'] = []  # list of tuples: (op, obj, changed attribute, new value)
    system['hidden_rule'] = hidden_rule
    system['scratchpad'] = []  # to store user thoughts and report submissions
    run_initial_operations(system, n_initial_ops)
    return system

def show_last_changed(system):
    print("\nLast changed attributes for each object:")
    for obj in system['objects']:
        if obj['last_changed']:
            changes = obj['last_changed']
            if len(changes) == 1:
                change_str = f"{changes[0][0]} = {changes[0][1]:.5g}"
            else:
                change_str = f"{changes[0][0]} = {changes[0][1]:.5g} and others"
        else:
            change_str = "No changes yet"
        print(f"  {obj['name']}: {change_str}")
    print()

def show_history_table(system):
    history = system['history']
    if not history:
        print("\nNo operations have been performed yet!\n")
        return
    print("\nOperation History:")
    header = f"{'Op#':<4} {'Operation':<15} {'Object':<15} {'Changes':<30}"
    print(header)
    print("-" * len(header))
    for i, entry in enumerate(history, start=1):
        op, obj, attr, new_value = entry
        changes_str = f"{attr} = {new_value:.5g}"
        print(f"{i:<4} {op['name']:<15} {obj['name']:<15} {changes_str:<30}")
    print()

# --- Custom input functions to prevent stray key echoes ---
def getch():
    try:
        import msvcrt
        ch = msvcrt.getch()
        if isinstance(ch, bytes):
            return ch.decode("utf-8")
        else:
            return ch
    except ImportError:
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def read_menu_choice():
    valid = set("12345678")
    while True:
        ch = getch()
        if ch in valid:
            return ch

def read_thoughts_and_command(prompt):
    # Read a full line; extract trailing digit(s) as the command.
    text = input(prompt)
    m = re.search(r'(\d+)\s*$', text)
    if m:
        command = m.group(1)
        thoughts = text[:m.start()].strip()
    else:
        command = ""
        thoughts = text.strip()
    return thoughts, command

def read_multiline_report():
    print("Enter your report below. End your input with a line containing only a single period ('.').")
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines)

def run_interactive_ui():
    # Welcome message (each sentence separately).
    print("You are a talented scientist studying a new field of science.")
    print("Your task is to understand the things in this field and characterize their properties.")
    print("You have a number of objects available to study.")
    print("You can perform experiments on these objects to learn more about them.\n")
    # Scratchpad instruction.
    print("Note: A scratchpad is available to record your thoughts. In any input, the final character(s) represent your selection, and your full entry will be recorded.\n")
    # Hidden rule prompt.
    print("Examples:")
    print("  x = 3 * y + 5")
    print("  a = a * 2 if a > 0 else a")
    print("Use standard Python syntax. (Leave blank for no rule.)")
    hidden_rule = input().strip()
    if hidden_rule == "":
        hidden_rule = None
    # Run setup.
    s = setup_system(hidden_rule)
    # Setup message.
    print("\nThe experiments you can perform are as follows:")
    print("You can wuzzle objects.")
    print("You can splorficate objects.")
    # Instruction message.
    print("\nYou can instruct me, your lab assistant, to perform an experiment.")
    print("Perform as many experiments as you need to fully characterize the system, then write a report on your findings.")
    print("Good luck!\n")
    
    while True:
        print("========== Menu ==========")
        print("1) Show Objects")
        print("2) Show Possible Operations")
        print("3) Perform an Operation")
        print("4) Show Last Changed Attributes")
        print("5) Show Operation History (table format)")
        print("6) Show Scratchpad")
        print("7) Submit Report")
        print("8) Quit")
        print("==========================")
        print("Enter a command (1-8): ", end="", flush=True)
        choice = read_menu_choice()
        print()  # Newline after menu selection.
        if choice == '1':
            print_objects(s)
        elif choice == '2':
            print("\nHere are the possible operations:")
            for i, op in enumerate(s['ops']):
                print(f"  {i+1}. {op['name']}")
            print()
        elif choice == '3':
            if not s['objects']:
                print("No objects available!")
                continue
            if not s['ops']:
                print("No operations available!")
                continue
            print("\nWhich object do you want to apply an operation to?")
            for i, obj in enumerate(s['objects']):
                print(f"  {i+1}. {obj['name']}")
            # Reminder: final character is your selection.
            thoughts, obj_command = read_thoughts_and_command("Enter object number (final character is your selection, with any comments): ")
            s['scratchpad'].append("Object selection: " + thoughts + " (Selection: " + obj_command + ")")
            try:
                obj_index = int(obj_command) - 1
                chosen_obj = s['objects'][obj_index]
            except:
                print("Invalid object choice!\n")
                continue
            print("\nWhich operation do you want to perform?")
            for i, op in enumerate(s['ops']):
                print(f"  {i+1}. {op['name']}")
            thoughts, op_command = read_thoughts_and_command("Enter operation number (final character is your selection, with any comments): ")
            s['scratchpad'].append("Operation selection: " + thoughts + " (Selection: " + op_command + ")")
            try:
                op_index = int(op_command) - 1
                chosen_op = s['ops'][op_index]
            except:
                print("Invalid operation choice!\n")
                continue
            apply_operation(s, chosen_obj, chosen_op)
        elif choice == '4':
            show_last_changed(s)
        elif choice == '5':
            show_history_table(s)
        elif choice == '6':
            print("\nScratchpad:")
            for entry in s['scratchpad']:
                print("  " + entry)
            print()
        elif choice == '7':
            print("\nSubmit Report")
            print("Write your report of findings. Equations should follow this format (html):\n")
            print("<op>")
            print('"wuzzle"')
            print("</op>")
            print("<eq>")
            print("f(x) = 3 * x")
            print("</eq>")
            print("\n<vars>")
            print('<var>x = "zibblosity"</var>')
            print("</vars>\n")
            print("Enter your report. (You may use returns; end your input with a line containing only a single period '.'):")
            report = read_multiline_report()
            s['scratchpad'].append("Report submission: " + report + " (Final character: " + (report[-1] if report else "") + ")")
            if s['hidden_rule'] is not None:
                if s['hidden_rule'] in report:
                    print("Your report appears to include the underlying equation.")
                else:
                    print("Your report does not seem to match the underlying equation.")
            else:
                print("No underlying equation was specified.")
            print("Report submitted. Exiting.\n")
            sys.exit(0)
        elif choice == '8':
            print("Goodbye! Thanks for exploring.")
            sys.exit(0)

def run():
    s = setup_system()
    print("Welcome!")
    print("Here is the list of objects you have on hand. You can acquire more by requesting them.")
    print_objects(s)
    print()
    return s

if __name__ == "__main__":
    run_interactive_ui()

# The following interactive shell has been removed so that quitting exits Python.
# import code; code.interact(local=locals())

def spelling():
    # (for emacs, ignore)
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