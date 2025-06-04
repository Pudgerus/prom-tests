"""
Модуль тестирования функциональности класса Calculator.
"""

import unittest
from calculator import Calculator


class CalculatorTestCase(unittest.TestCase):
    """Тест-кейс для проверки работы Calculator."""

    def setUp(self):
        self.calc = Calculator()

    def test_basic_arithmetic(self):
        """Арифметика: сложение, вычитание, умножение, деление."""
        test_cases = [
            ("2 + 2", 4),
            ("5 - 3", 2),
            ("4 * 3", 12),
            ("10 / 2", 5),
        ]
        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                self.assertEqual(self.calc.calculate(expression), expected)

    def test_precedence_and_parentheses(self):
        """Приоритеты операторов и скобки."""
        test_cases = [
            ("2 + 3 * 4", 14),
            ("(2 + 3) * 4", 20),
            ("10 - 4 / 2", 8),
        ]
        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                self.assertEqual(self.calc.calculate(expression), expected)

    def test_zero_division(self):
        """Деление на ноль вызывает ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.calculate("5 / 0")

    def test_invalid_inputs(self):
        """Некорректные выражения вызывают ValueError."""
        invalid_expressions = ["2 +", "(2 + 3", "2 & 3"]
        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    self.calc.calculate(expr)

    def test_infix_to_postfix(self):
        """Преобразование инфиксной записи в постфиксную."""
        test_cases = [
            ("2 + 3", "2 3 +"),
            ("2 + 3 * 4", "2 3 4 * +"),
        ]
        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                tokens = self.calc._tokenize(expression)
                postfix = self.calc._to_postfix(tokens)
                self.assertEqual(' '.join(postfix), expected)


if __name__ == "__main__":
    unittest.main()
