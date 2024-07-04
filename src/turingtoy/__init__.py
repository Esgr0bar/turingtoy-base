from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)

def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List[Dict[str, str]], bool]:
    blank = machine['blank']
    start_state = machine['start state']
    final_states = set(machine['final states'])
    table = machine['table']
    
    tape = list(input_)
    current_state = start_state
    current_position = 0
    execution_history = []

    step_count = 0

    while steps is None or step_count < steps:
        if current_position < 0:
            tape.insert(0, blank)
            current_position = 0
        elif current_position >= len(tape):
            tape.append(blank)
        
        current_symbol = tape[current_position]
        state_transitions = table.get(current_state, {})
        transition = state_transitions.get(current_symbol)

        if transition is None:
            break

        history_entry = {
            'state': current_state,
            'reading': current_symbol,
            'position': current_position,
            'memory': ''.join(tape),
            'transition': transition,
        }
        execution_history.append(history_entry)

        if isinstance(transition, str):
            if transition == 'R':
                current_position += 1
            elif transition == 'L':
                current_position -= 1
        elif isinstance(transition, dict):
            if 'write' in transition:
                tape[current_position] = transition['write']
            if 'R' in transition:
                current_position += 1
                current_state = transition['R']
            elif 'L' in transition:
                current_position -= 1
                current_state = transition['L']

        step_count += 1

        if current_state in final_states:
            break
    
    output = ''.join(tape).strip(blank)
    accepted = current_state in final_states

    return output, execution_history, accepted
