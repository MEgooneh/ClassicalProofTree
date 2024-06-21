class Operator:
    priority = None

class NotOperator(Operator):
    priority = 0
    
    def __str__(self):
        return "¬"

class AndOperator(Operator):
    priority = 1
    
    def __str__(self):
        return "∧"

class OrOperator(Operator):
    priority = 2
    
    def __str__(self):
        return "∨"

class ImplicationOperator(Operator):
    priority = 3
    
    def __str__(self):
        return "→"

class LeftParenthesisOperator(Operator):
    priority = 4
    
    def __str__(self):
        return "("

class RightParenthesisOperator(Operator):
    priority = 5
    
    def __str__(self):
        return ")"



class Atom:
    def __init__(self, name: str):
        self.__name = name
            
    def __str__(self):
        return self.__name
    
class Universe:
    Atoms = dict()
    singleton = None
    def __init__(self):
        if singleton:
            raise "Universe is a singleton class"
        singleton = True

    @staticmethod
    def get_atom(name: str) -> Atom:
        if name not in Universe.Atoms.keys():
            Universe.Atoms[name] = Atom(name)
        return Universe.Atoms[name]


class Expression:
    operators = {
        '¬': NotOperator(),
        '∧': AndOperator(),
        '∨': OrOperator(),
        '→': ImplicationOperator(),
        '(': LeftParenthesisOperator(),
        ')': RightParenthesisOperator()
    }
    def __init__(self, expression: str = "", postfixed_exp: list = []):
        if expression:
            self.__init__expression(expression)
        elif postfixed_exp:
            self.__init__postfixed(postfixed_exp)
        else:
            raise "Not enough arguments"

    def __init__expression(self, expression: str):
        cleaned_expression = self.clean(expression)
        self.__splitted_exp = self.split(cleaned_expression)
        self.__postfixed_exp = self.postfixer(self.__splitted_exp)
        self.__expression = self.normal_form(self.__postfixed_exp)

    def __init__postfixed(self, postfixed_exp: list):
        self.__postfixed_exp = postfixed_exp
        self.__expression = self.normal_form(self.__postfixed_exp)
        self.__splitted_exp = []
        for i in postfixed_exp:
            if isinstance(i, Atom):
                self.__splitted_exp.append(i)
            else:
                self.__splitted_exp.append(str(i))

    def __str__(self):
        return self.__expression

    def clean(self, s: str) -> str:
        s = s.replace(' ', '')
        return s
    
    def split(self, s: str) -> list:
        splitted_list = []
        chunk = ''
        for i in s:
            if i in self.operators.keys():
                if chunk:
                    splitted_list.append(Universe.get_atom(chunk))
                chunk = ''
                splitted_list.append(self.operators[i])
            else:
                chunk += i
        if chunk:
            splitted_list.append(Universe.get_atom(chunk))
        splitted_list = [i for i in splitted_list if i != '']
        return splitted_list
    
    def postfixer(self, splitted_exp: list) -> list:
        stack = []
        postfixed_exp = []
        for i in splitted_exp:
            if isinstance(i, Operator):
                if isinstance(i, LeftParenthesisOperator):
                    stack.append(i)
                elif isinstance(i, RightParenthesisOperator):
                    while isinstance(stack[-1], LeftParenthesisOperator) == False:
                        postfixed_exp.append(stack.pop())
                    stack.pop()
                else:
                    while stack and stack[-1].priority < i.priority:
                        postfixed_exp.append(stack.pop())
                    stack.append(i)
            else:
                postfixed_exp.append(i)
        while stack:
            postfixed_exp.append(stack.pop())
        return postfixed_exp

    def normal_form(self, postfixed_exp: list) -> str:
        stack = []
        for i in postfixed_exp:
            if isinstance(i, Operator):
                if isinstance(i, NotOperator):
                    stack.append(str(i) + str(stack.pop()))
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(f'({b}{i}{a})')
            else:
                stack.append(str(i))
        return stack[0]
    
    def get_postfixed(self) -> list:
        return self.__postfixed_exp

    def get_splitted(self) -> list:
        return self.__splitted_exp

    def get_sequence(self) -> list:
        sequence = []
        stack = []
        for i in self.__postfixed_exp:
            if isinstance(i, Operator):
                if isinstance(i, NotOperator):
                    stack.append(str(i) +  stack.pop())
                    sequence.append(stack[-1])
                else:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(f'({b}{i}{a})')
                    sequence.append(stack[-1])
            else:    
                stack.append(i)
                sequence.append(i)

            if sequence.count(stack[-1]) > 1:
                sequence.pop()
        return sequence
    
    def is_atomic(self) -> bool :
        return len(self.__postfixed_exp) == 1 or (len(self.__postfixed_exp) == 2 and isinstance(self.__postfixed_exp[1], NotOperator))