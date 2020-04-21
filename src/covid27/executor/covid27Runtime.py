import sys
import traceback

from covid27.common.constants import Constants

class Runtime:
    def __init__(self, interim_code_path):
    
        self.double_stack = []
        self.bool_stack = []
        self.string_stack = []
        self.list_name_stack = []
        self.double_list_stack = []

        self.double_map = {}
        self.bool_map = {}
        self.string_map = {}
        self.double_list_map = {}
        self.interim_code_path = interim_code_path
        self.f = open(interim_code_path)
        self.interim_code = iter(self.f)

    def get_next_instruction(self, label):
        try:
            line = next(self.interim_code)
            if label == '':
                return line
            else:
                while not line.startswith(label):
                    line = next(self.interim_code)
                return line
        except Exception as e:
            print(str(e))
        return ""

    def checkFloat(self, val):
        try:
            float(val)
            return True
        except:
            return False
            

    def execute(self):
        var_list = []
        double_list = []
        try:
            line = self.get_next_instruction('')
            take_line_flag = True
            while line != '':
                cmd = line.split()[0]
                if cmd == Constants.STORE:
                    var_name = line.split()[1]
                    if var_name in self.double_map:
                        d = self.double_stack.pop()
                        self.double_map[var_name] = d
                        self.double_stack.append(d)
                    elif var_name in self.bool_map:
                        b = self.bool_stack.pop()
                        self.bool_map[var_name] = b
                        self.bool_stack.append(b)
                    elif var_name in self.string_map:
                        s = self.string_stack.pop()
                        self.string_map[var_name] = s
                        self.string_stack.append(s)
                    elif var_name in self.double_list_map:
                        new_double_list = list(self.double_list_stack.pop())
                        self.double_list_map[var_name] = new_double_list
                        self.double_list_stack.append(new_double_list)
                elif cmd == Constants.LOAD:
                    s = line.split()[1]
                    if s in self.double_map:
                        self.double_stack.append(self.double_map[s])
                    elif s in self.bool_map:
                        self.bool_stack.append(self.bool_map[s])
                    elif s in self.string_map:
                        self.string_stack.append(self.string_map[s])
                    elif s in self.double_list_map:
                        self.double_list_stack.append(self.double_list_map[s])
                elif cmd == Constants.EQB:
                    first_val = self.bool_stack.pop()
                    second_val = self.bool_stack.pop()
                    self.bool_stack.append(first_val == second_val)
                elif cmd == Constants.NEQ:
                    first_val = self.double_stack.pop()
                    second_val = self.double_stack.pop()
                    self.bool_stack.append(first_val != second_val)
                elif cmd == Constants.EQ:
                    first_val = self.double_stack.pop()
                    second_val = self.double_stack.pop()
                    self.bool_stack.append(first_val == second_val)
                elif cmd == Constants.NEQB:
                    second_val = self.bool_stack.pop()
                    first_val = self.bool_stack.pop()
                    self.bool_stack.append(first_val != second_val)
                elif cmd == Constants.LT:
                    second_val = self.double_stack.pop()
                    first_val = self.double_stack.pop()
                    self.bool_stack.append(first_val < second_val)
                elif cmd == Constants.LTE:
                    second_val = self.double_stack.pop()
                    first_val = self.double_stack.pop()
                    self.bool_stack.append(first_val <= second_val)
                elif cmd == Constants.GT:
                    second_val = self.double_stack.pop()
                    first_val = self.double_stack.pop()
                    self.bool_stack.append(first_val > second_val)
                elif cmd == Constants.GTE:
                    second_val = self.double_stack.pop()
                    first_val = self.double_stack.pop()
                    self.bool_stack.append(first_val >= second_val)
                elif cmd == Constants.AND:
                    second_val = self.bool_stack.pop()
                    first_val = self.bool_stack.pop()
                    self.bool_stack.append(first_val and second_val)
                elif cmd == Constants.OR:
                    second_val = self.bool_stack.pop()
                    first_val = self.bool_stack.pop()
                    self.bool_stack.append(first_val or second_val)
                # TODO: Complete the command structure!
                if take_line_flag:
                    line = self.get_next_instruction('')
        except Exception as e:
            print('Runtime Error:', e)
            traceback.print_exc()
                