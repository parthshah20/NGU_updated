from gekko import GEKKO
from sympy import *
import re

class Solution():
    def __init__(self):
        self.equations = []
        self.variables = []
        self.num_equations = 0
        self.constants = []
        self.const_value = {}

    def process_equations(self, equations):
        # for i in range(len(equations)):
        #     equations[i] = re.sub(r'e\*\*', 'e', equations[i])
        equations = [x.replace('=', '==') for x in equations]
        equations = [x.replace('sin', '_m.sin') for x in equations]
        equations = [x.replace('cos', '_m.cos') for x in equations]
        equations = [x.replace('tan', '_m.tan') for x in equations]
        equations = [x.replace('sqrt', '_m.sqrt') for x in equations]
        equations = [x.replace('log', '_m.log') for x in equations]
        equations = [x.replace('ln', '_m.log') for x in equations]
        equations = [x.replace('exp', '2.718281828459') for x in equations]
        equations = [x.replace('pi', '_m.pi') for x in equations]
        equations = [x.replace('e', '2.718281828459') for x in equations]
        equations = [x.replace('E', '2.718281828459') for x in equations]
        return equations

    def get_variables(self, equations):
        var_pattern = re.compile(r'\b[a-zA-Z]+\w*\d*\b')
        variables = []
        for i in range(len(equations)):
            variables += var_pattern.findall(equations[i])
        self.variables = list(set(variables))
        to_remove = ['sin', 'cos', 'tan', 'sqrt',
                    'log', 'ln', 'exp', 'pi', 'e']
        for i in range(len(to_remove)):
            if to_remove[i] in self.variables:
                self.variables.remove(to_remove[i])

    # Define the constants with '_' at the start and the end of names

    def get_constants(self, equations):
        var_pattern = re.compile(r'\b_+[a-zA-Z]+\w*\d*_\b')
        constants = []
        for i in range(len(equations)):
            constants += var_pattern.findall(equations[i])
        self.constants = list(set(constants))
        self.constants = [str(var) for var in self.constants]

    # Function to replace the constants in the equations with their assigned values

    def replace_constants(self, equations):
        ans = []
        for eq in equations:
            for const in self.constants:
                if const in eq:
                    print((eq, const, self.const_value[const]))
                    eq = eq.replace(const, self.const_value[const])
                    print(eq)
            ans.append(eq)
        return ans
    
    # Function to fetch the values of constants from the corresponding file
    
    def get_const_values(self, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                temp = line.strip()
                for const in self.constants:
                    if const in temp:
                        self.const_value[const] = temp.split('=')[-1]
        print(self.const_value)
        return
    
    # Function to solve the equations and print the answers to a file

    def solution(self, equations, num_variables, const_file):
        equations = self.process_equations(equations)
        _m = GEKKO(remote=False)
        self.get_variables(equations)

        # --- Constant resolution
        self.get_constants(equations)
        self.get_const_values(const_file)
        equations = self.replace_constants(equations)


        var_names = [str(var) for var in self.variables]
        # Create variables
        exec_dict = {}
        for var_name in var_names:
            exec_dict[var_name] = _m.Var(1)
            exec(f"{var_name} = exec_dict['{var_name}']")

        # Create equations
        temp = ""
        for _x in equations:
            temp += _x + ','
        temp = temp[:-1]
        exec(f"_m.Equations([{temp}])")
        _m.solve(disp=True)
        # Retrieve variable values
        answers = [exec_dict[var].value for var in var_names]
        _d = {}
        for _ in range(len(var_names)):
            _d[var_names[_]] = answers[_]
        return _d

