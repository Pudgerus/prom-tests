"""Модуль для обработки инфиксных и постфиксных выражений."""


class Calculator:
    """Калькулятор, преобразующий инфиксные выражения и вычисляющий результат."""

    def __init__(self):
        self.ops_priority = {'+': 1, '-': 1, '*': 2, '/': 2}

    def _is_number_char(self, ch):
        return ch.isdigit() or ch == '.'

    def _tokenize(self, expr):
        i, tokens = 0, []
        while i < len(expr):
            ch = expr[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit() or ch == '.':
                start = i
                while i < len(expr) and self._is_number_char(expr[i]):
                    i += 1
                tokens.append(expr[start:i])
                continue
            tokens.append(ch)
            i += 1
        return tokens

    def _to_postfix(self, tokens):
        result, stack = [], []
        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                result.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    result.append(stack.pop())
                if not stack:
                    raise ValueError("Несогласованные скобки")
                stack.pop()
            else:
                if token not in self.ops_priority:
                    raise ValueError(f"Неизвестный оператор: {token}")
                while (stack and stack[-1] != '(' and
                       self.ops_priority[stack[-1]] >= self.ops_priority[token]):
                    result.append(stack.pop())
                stack.append(token)
        while stack:
            if stack[-1] == '(':
                raise ValueError("Несогласованные скобки")
            result.append(stack.pop())
        return result

    def _evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов")
                b = stack.pop()
                a = stack.pop()
                match token:
                    case '+':
                        stack.append(a + b)
                    case '-':
                        stack.append(a - b)
                    case '*':
                        stack.append(a * b)
                    case '/':
                        if b == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        stack.append(a / b)
                    case _:
                        raise ValueError(f"Неизвестный оператор: {token}")
        if len(stack) != 1:
            raise ValueError("Ошибка вычисления: лишние операнды")
        return stack[0]

    def calculate(self, expression):
        tokens = self._tokenize(expression)
        postfix = self._to_postfix(tokens)
        return self._evaluate_postfix(postfix)
