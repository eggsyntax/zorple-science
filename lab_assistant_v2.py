import re
import json
from domain_generator.system import setup_system, print_objects
from domain_generator.operations import apply_operation

def parse_llm_output(output_string):
    '''
    parses the output string and create a list of experiments to be done.
    LLM is instructed to follow the format specified in setup_string_v2() in system.py
    '''
    def find_all_matches(pattern, string, group=0):
        pat = re.compile(pattern)
        pos = 0
        out = []
        m = pat.search(string, pos)
        while m:
            pos = m.start() + 1
            out.append(m[group])
            m = pat.search(string, pos)
        return out
    
    # pattern = r"{\"op_name\":(\_)?\"[a-zA-Z0-9\-]*\", \"obj1_name\": \"[a-zA-Z0-9\-]*\"(, \"obj2_name\": \"[a-zA-Z0-9\-]*\")?}"
    # pattern = r"((\[[^\}]{3,})?\{s*[^\}\{]{3,}?:.*\}([^\{]+\])?)"
    pattern = r'{\s*"op_name"\s*:\s*"\s*(F-\d{3})\s*"\s*,\s*"obj1_name"\s*:\s*"\s*(O-\d{3})\s*"\s*}'
    exp_list = find_all_matches(pattern, output_string)
    exp_list = [json.loads(exp) for exp in exp_list]

    # exp_list = [{'obj_name':'snigglet7579', 'op_name':'wuzzle'}]
    return exp_list

def run_experiments(system, experiment_list):
    '''
    Runs the experiments specified in the experiment_list on the given system.
    Each experiment is a dictionary with 'obj_name' and 'op_name' keys.
    The function returns a list of outcome strings and a tuple indicating the range of indices in the system's history that correspond to the experiments.
    '''
    
    result_template = "Applying {op_name} to object {obj_name} changed the value of its {property} from {old_val} to {new_val}."
    no_change_template = "Applying {op_name} to object {obj_name} did not change anything."
    outcomes = []

    exp_ind_start = len(system['history'])
    exp_ind_end = -1

    for exp in experiment_list:
        obj1_name, obj2_name, op_name = exp['obj1_name'], None, exp['op_name']
        if 'obj2_name' in exp:
            obj2_name = exp['obj2_name']
        obj1, obj2, op = None, None, None

        for object in system['objects']:
            if object['name'] == obj1_name:
                obj1 = object
            elif object['name'] == obj2_name:
                obj2 = object   

        for operation in system['operations']:
            if operation['name'] == op_name:
                op = operation
                break

        if obj1 == None:
            raise ValueError(f'Object {obj1_name} does not exist!')
        # if obj2 == None:
        #     raise ValueError(f'Object {obj2_name} does not exist!')
        if op == None:
            raise ValueError(f'Operation {op_name} does not exist!')
        
        if op['operation_type'] == 'unary':

            old_val = None
            if op['target_property']['name'] in obj1['properties']:
                old_val = obj1['properties'][op['target_property']['name']]
            
            flag = apply_operation(system, obj1, op)

            if flag == 1:
                result = result_template.format(
                    op_name = op_name,
                    obj_name = obj1_name,
                    property = op['target_property']['name'],
                    old_val = old_val,
                    new_val = system['history'][-1][1]['properties'][op['target_property']['name']]
                )
            else:
                result = no_change_template.format(
                    op_name = op_name,
                    obj_name = obj1_name,
                )

        elif op['operation_type'] == 'binary':
            old_val = None
            if op['first_target']['name'] in obj1['properties']:
                old_val = obj1['properties'][op['first_target']['name']]
            
            flag = apply_operation(system, obj1, op, obj2=obj2)

            if flag == 1:
                result = result_template.format(
                    op_name = op_name,
                    obj_name = obj1_name,
                    property = op['first_target']['name'],
                    old_val = old_val,
                    new_val = system['history'][-1][1]['properties'][op['first_target']['name']]
                )
            else:
                result = no_change_template.format(
                    op_name = op_name,
                    obj_name = obj1_name,
                )

        outcomes.append(result)

    exp_ind_end = len(system['history'])
    return outcomes, (exp_ind_start, exp_ind_end)

def format_experiment_outputs(outcomes):
    '''
    Formats the outcomes of the experiments into a readable string.
    '''
    
    outcome_str = 'The results of the requested experiments are as follows:\n'
    outcome_str += '\n'.join(outcomes)
    return outcome_str


def lab_assistant(system, llm_output):

    end_str = '\nYou can either perform more experiments or summarize your findings as a report.'
    exp_list = parse_llm_output(llm_output)
    print('Experiment list', exp_list)

    if len(exp_list) == 0:
        raise Exception('No experiments')
    
    outcomes, _ = run_experiments(system, exp_list)
    outcome_str = format_experiment_outputs(outcomes)
    outcome_str += end_str

    return outcome_str


def setup_string_v2(system):
    unary_ops, binary_ops = [], [] 
    for op in system['operations']:
        if op['operation_type'] == 'unary':
            unary_ops.append(op['name'])
        elif op['operation_type'] == 'binary':
            binary_ops.append(op['name'])
     
    format_unary = '{ind}. {verb}: {{"op_name":"{verb}, "obj1_name": "<object name>"}}'
    format_binary = '{ind}. {verb}: {{"op_name":"{verb}, "obj1_name": "<object name>", "obj2_name": "<object name>", "}}'

    exp_formats = []
    i = 0
    for name in unary_ops:
        i += 1
        exp_formats.append(format_unary.format(ind=i, verb=name))
    for name in binary_ops:
        i += 1
        exp_formats.append(format_binary.format(ind=i, verb=name))
    exp_formats = '\n'+'\n'.join(exp_formats)+'\n'
        
    s = (f'You are a talented scientist. You have begun to study a brand new field of science, and it is your task to '
         f'understand the sorts of things in this field and characterize their properties. You have a number of objects '
        #  f'available to study. You can perform experiments on these objects to learn more about them. The experiments '
         f'available to study. You can perform experiments on these objects to learn more about them. The experiments you can perform are either unary operations or binary operations. Unary operations act on a single object.' 
         f'Here is the list of unary operations: {unary_ops}. Binary operations act on the first object based on the second object. These are not commutative. Here is the list of binary operations: {binary_ops}.'
         f'You can perform an experiment by just telling me, your lab assistant, to perform them. '
         f'You can request any experiment in the following JSON format:'
         f'{exp_formats}'
         f'Strictly adhere to this format and request me to perform the experiments. '
         f'Perform as many experiments as you need to in order '
         f'to be confident you can characterize the system scientifically as fully as possible. Then write a report on your '
         f'findings. Good luck!')
    return s

def run():
    system = setup_system(num_types=2, num_objects=4, num_operations=10)
    print(setup_string_v2(system))
    print_objects(system)
    # llm_output =  """Let me try these experiments! \n {"op_name": "F-003", "obj1_name": "O-003"}, {"op_name": "F-001", "obj1_name": "O-001", "obj2_name": "O-003"}"""

    llm_output = """Let me start by sending the first experiment: F-002 on O-001.
To begin understanding the effects of the unary operations, I'll start by applying F-002 to O-001.

**Experiment 1:**
```json
{
  "op_name": "F-002",
  "obj1_name": "O-001"
}"""
    outcome_str = lab_assistant(system, llm_output)
    print(outcome_str)


if __name__ == '__main__':
    run()
