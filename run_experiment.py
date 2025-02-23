from domain_generator.system import setup_system, print_objects
from lab_assistant_v2 import setup_string_v2, lab_assistant
from api import Conversation
import os
import pprint
from datetime import datetime


def get_first_prompt(system):

    prompt = setup_string_v2(system)
    prompt += '\n'
    prompt += print_objects(system)
    return prompt


def run_exp(system, model, log):

    log.write('Operations in the systems\n')
    operations = pprint.pformat(system['operations'])
    log.writelines(operations+'\n\n')
    log.write('\n'+'*'*40+'\n')

    first_prompt = get_first_prompt(system)
    print(first_prompt)
    log.write('Conversation\n\n')
    log.writelines(first_prompt)
    log.write('\n'+'*'*40+'\n')

    
    sci_agent = Conversation(model)
    n_tries = 3

    prompt = first_prompt
    for i in range(n_tries):

        response = sci_agent.message(msg=prompt, print_history=True)
        log.writelines(response)
        log.write('\n'+'*'*40+'\n')


        print('\n'+'*'*40+'\n'+response)

        outcome = lab_assistant(system, response)

        log.writelines(outcome)
        log.write('\n'+'*'*40+'\n')

        prompt = outcome

def main():

    now = str(datetime.now())

    # model = 'google/gemma-2-9b-it:free'
    model = 'deepseek/deepseek-r1-distill-llama-70b:free'
    # model = 'deepseek/deepseek-r1:free'

    directory = 'transcripts'
    filename = f"{model.split('/')[-1]}_{now}.txt"
    filepath = os.path.join(directory, filename)
    log = open(filepath, 'w')

    system = setup_system(num_types=1, num_objects=4, num_operations=5)

    run_exp(system, model, log)


if __name__ == '__main__':
    main()


