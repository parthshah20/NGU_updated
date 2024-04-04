import gekko_solver
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--equations', type=str, default='_Equations1.txt')
parser.add_argument('--constants', type=str, default='constants.txt')
parser.add_argument('--answers', type=str, default='_Answers.txt')
args = parser.parse_args()


def run(eq_file, const_file, answer_file):
    equations = []
    equations_file = eq_file
    with open(equations_file, 'r') as f:
        for line in f:
            equations.append(line.strip())

    s = gekko_solver.Solution()

    # write answers to file 
    answers_file = answer_file
    start_time = time.time()
    answers = s.solution(equations, len(equations), const_file)
    end_time = time.time()

    with open(answers_file, 'w') as f:
        total_time = end_time - start_time
        f.write(f'Total time: {total_time} seconds\n')
        for key, value in answers.items():
            var_name = key
            var_value = value[0]
            # write to the file
            f.write(f'{var_name} = {var_value}\n')