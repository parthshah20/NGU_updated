import gekko_solver
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--equations', type=str, default='_Equations1.txt')
parser.add_argument('--constants', type=str, default='_Coefficient.txt')
parser.add_argument('--answers', type=str, default='_Answers.txt')
args = parser.parse_args()

class file_names():
    def __init__(self):
        self.show = 0
        self.file = ["_Equations.txt", "_Answers.txt", "_Coefficient.txt"]
    def change_name(self, idx, name):
        self.file[idx] = name
    def return_name(self, idx):
        return self.file[idx]

name_dict = file_names()

def run(eq_file, const_file, answer_file):
    equations = []
    coeff_equations = []
    equations_file = eq_file
    with open(equations_file, 'r') as f:
        for line in f:
            if line == '' or line == ' ' or line == '\n':
                print("Here")
                continue
            equations.append(line.strip())
    # try:
    #     if const_file != None:
    #         with open(const_file, 'r') as f:
    #             for line in f:
    #                 if line == '' or line == ' ' or line == '\n':
    #                     print("Here")
    #                     continue
    #                 equations.append(line.strip())
    # except:
    #     print("No coefficient file")
    
    if equations == []:
        with open(answer_file, 'w') as f:
            f.write('')
        return

    s = gekko_solver.Solution(coeff=(const_file == None))

    # write answers to file 
    answers_file = answer_file
    start_time = time.time()
    answers = s.solution(equations, len(equations), const_file)
    end_time = time.time()

    with open(answers_file, 'w') as f:
        # total_time = end_time - start_time
        # f.write(f'Total time: {total_time} seconds\n')
        for key, value in answers.items():
            var_name = key
            if var_name[0] == '_' and (const_file!=None):
                continue
            var_value = value[0]
            # write to the file
            f.write(f'{var_name} = {var_value}\n')