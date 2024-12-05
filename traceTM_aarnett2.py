import csv
from collections import deque, defaultdict

# initialize NTM
class NTM:
    def __init__(self, filename, output_file):
        self.transitions = defaultdict(list)
        self.load_machine(filename)
        self.output_file = output_file


    def load_machine(self, filename):
        # parse CSV file

        with open(filename) as f:
            # load information from header
            reader = csv.reader(f)
            self.name = next(reader)[0]
            self.states = next(reader)
            self.alphabet = next(reader)
            self.tape_symbols = next(reader)
            self.start_state = next(reader)[0]
            self.accept_state = next(reader)[0]
            self.reject_state = next(reader)[0]

            # read transitins
            for row in reader:
                state, input_char, next_state, write_char, direction = row
                self.transitions[(state, input_char)].append((next_state, write_char, direction))

    # log to output file and print to console
    def log(self, message):
        with open(self.output_file, "a") as f:
            f.write(message + "\n")
        print(message)

    # simulate NTM
    def run(self, input_string, max_steps=1000):

        # initial configuration
        queue = deque([("", self.start_state, input_string)])
        tree = [[("", self.start_state, input_string)]]
        steps = 0
        total_configurations = 0
        accept_found = False

        self.log(f"Machine Name: {self.name}")
        self.log(f"Input String: {input_string}")

        while queue and steps < max_steps:
            next_level = []
            current_nonleaves = len(queue)
            total_configurations += len(queue)
            steps += current_nonleaves
            for left, state, right in queue:

                # check for accept state
                if state == self.accept_state:
                    accept_found = True
                    self.log(f"String accepted")
                    self.log(f"Depth of the tree: {len(tree)}")
                    self.log(f"Total configurations explored: {total_configurations}")
                    self.print_path(tree, left, state, right)
                    self.print_nondeterminism(tree)
                    return
                
                # check for reject state
                if state == self.reject_state:
                    continue

                # get current character under tape head
                current_char = right[0] if right else "_"

                # fetch possible transitions
                possible_moves = self.transitions.get((state, current_char), [])
                for next_state, write_char, direction in possible_moves:
                   
                    # update the tape
                    new_left, new_right = list(left), list(right)
                    if direction == "R":
                        new_left.append(write_char)
                        new_right = new_right[1:] if len(new_right) > 1 else ["_"]
                    elif direction == "L":
                        new_right.insert(0, write_char)
                        new_left = new_left[:-1] if new_left else ["_"]
                    
                    # add new config to the next level
                    new_config = ("".join(new_left), next_state, "".join(new_right))
                    next_level.append(new_config)

            queue = deque(next_level)
            tree.append(next_level)
        
        # string is rejected
        if not accept_found:
            self.log(f"String rejected after {len(tree)} steps")
            self.print_nondeterminism(tree)

        # steps exceed max 
        if steps >= max_steps:
            self.log(f"Execution stopped after {max_steps} transitions.")
    
    # trace path from start config to accepting state
    def print_path(self, tree, left, state, right):
        self.log("Path to accept state:")
        for level in tree:
            for config in level:
                self.log(f"Left: {config[0]}, State: {config[1]}, Head: {config[2]}")
        self.log(f"Final Configuration: Left: {left}, State: {state}, Head: {right}")
    
    # calculate and print measure of nondeterminism
    def print_nondeterminism(self, tree):
        total_transitions = sum(len(level) for level in tree)
        total_nonleaves = sum(1 for level in tree for config in level if len(self.transitions.get((config[1], config[2][0] if config[2] else "_"), [])) > 0)
        nondeterminism = total_transitions / total_nonleaves if total_nonleaves > 0 else 1
        self.log(f"Measure of Nondeterminism: {nondeterminism:.2f}")
        self.log("\n")