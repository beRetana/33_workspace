# input_processor.py
import sys
import time
from unittest import case

from grin import lexing, location, parsing, token as t, GrinParseError, GrinLexError, GrinToken
from grin.interpreter.interpreter import Interpreter
from grin.interpreter.commads import *

_FIRST_COMMAND = 0

class InputProcessor:

    def __init__(self):
        self._interpreter = Interpreter()
        self._line_count = 0
        self._temp_index = 0
        self._running = True

    def interpreter(self):
        """@return The interpreter object of the class."""
        return self._interpreter

    def line_count(self):
        """@return The line count of the interpreter."""
        return self._line_count

    @staticmethod
    def is_numeric(value: int|float|str)->bool:
        """@return Whether the value is numeric."""
        return type(value) is int or type(value) is float

    @staticmethod
    def construct_operation(value: t.GrinTokenKind):
        """Creates a lambda expression from a string."""

        match value:
            case t.GrinTokenKind.LESS_THAN:
                return lambda first, second : first < second
            case t.GrinTokenKind.GREATER_THAN:
                return lambda first, second: first > second
            case t.GrinTokenKind.LESS_THAN_OR_EQUAL:
                return lambda first, second: first <= second
            case t.GrinTokenKind.GREATER_THAN_OR_EQUAL:
                return lambda first, second: first >= second
            case t.GrinTokenKind.EQUAL:
                return lambda first, second: first == second
            case t.GrinTokenKind.NOT_EQUAL:
                return lambda first, second: first != second

    def check_primitive_numeric_str(self, first_value, second_value, action) -> str | int | float | None:
        """ @param first_value: str | int | float
            @param second_value: str | int | float
            @param action: function of two parameters
            @return The new value after applying the action or None if value error occurred!
        """
        try:
            if type(first_value) is int and type(second_value) is int:
                return int(action(first_value, second_value))
            return action(first_value, second_value)
        except ZeroDivisionError:
            self.end_program(f"Arithmetic Error for {first_value}/{second_value}")
        except TypeError:
            self.end_program(f"Type Error: {first_value}, and {second_value}")

    def check_right_types(self, first_token: GrinToken, second_token: GrinToken, action)-> str | int | float | None:
        """ @param first_token:
            @param second_token:
            @param action: function of two parameters
            @return The new value after applying the action or None if value error occurred!
        """
        first_var_value = self.is_variable_real(first_token.value())
        if not first_var_value: return

        if second_token.kind() == t.GrinTokenKind.IDENTIFIER:
            second_var_value = self.is_variable_real(second_token.value())
            if not second_var_value: return
            return self.check_primitive_numeric_str(first_var_value, second_var_value, action)
        else:
            return self.check_primitive_numeric_str(first_var_value, second_token.value(), action)

    def is_variable_real(self, var_name: str)-> str|int|float:
        """@return Whether the variable exists in the interpreter's stack."""
        result = self._interpreter.get_variable(var_name)
        if result is not None: return result
        return 0

    def on_let(self, line: list[GrinToken]) -> None:
        """Deals with the logic for when the token is a LET type"""
        value = 0
        if len(line) == 2:
            self._interpreter.add_variable(Identifier(line[1].value(), value))

        match line[2].kind():
            case t.GrinTokenKind.IDENTIFIER:
                result = self.is_variable_real(line[2].value())
                if result: value = result
                else: return
            case t.GrinTokenKind.LITERAL_INTEGER:
                value = int(line[2].value())
            case t.GrinTokenKind.LITERAL_FLOAT:
                value = float(line[2].value())
            case t.GrinTokenKind.LITERAL_STRING:
                value = line[2].value()
        self._interpreter.add_variable(Identifier(line[1].value(), value))

    def on_print(self, line: list[GrinToken]) -> None:
        """Deals with the logic for when the token is a PRINT type"""
        value = line[1].value()
        if line[1].kind() == t.GrinTokenKind.IDENTIFIER:
            value = self.is_variable_real(line[1].value())
        self._interpreter.print(Print(value))

    def on_arithmetic(self, line: list[GrinToken], action) -> None:
        """Deals with the logic for when subtracting tokens"""

        if not self.is_variable_real(line[1].value()): return
        new_var_value = self.check_right_types(line[1], line[2], action)
        if new_var_value: self._interpreter.add_variable(Identifier(line[1].value(), new_var_value))

    def on_comparison(self, line: list[GrinToken], action) -> None:
        """Deals with the logic for when subtracting tokens"""

        first_var_value = line[1].value()
        second_var_value = line[2].value()

        if line[1].kind() == t.GrinTokenKind.IDENTIFIER:
            first_var_value = self.is_variable_real(first_var_value)
        if line[2].kind() == t.GrinTokenKind.IDENTIFIER:
            second_var_value = self.is_variable_real(second_var_value)

        Comparison(first_var_value, second_var_value).evaluate(action)

    def on_goto(self, line: list[GrinToken]) -> None:
        """Deals with the logic for when the token is a GOTO type"""

        if len(line) > 2:
            first_value = line[3].value()
            operation = line[4].kind()
            second_value = line[5].value()

            if line[3].kind() == t.GrinTokenKind.IDENTIFIER:
                first_value = self.is_variable_real(first_value)
            if line[5].kind() == t.GrinTokenKind.IDENTIFIER:
                second_value = self.is_variable_real(second_value)

            if not Comparison(first_value, second_value).evaluate(self.construct_operation(operation)): return

        value = line[1].value()
        if line[1].kind() == t.GrinTokenKind.IDENTIFIER:
            value = self.is_variable_real(line[1].value())

        if type(value) is str:
            label = self._interpreter.get_label(value)
            if not label: return
            self._line_count = label-1
        if type(value) is int:
            if value == 0 or self._line_count+value-1 < 0 or value-1+self._line_count > self._temp_index:
                self.end_program("GOTO value index not Valid")
                return
            self._line_count += value-1

    def on_label(self, line: list[GrinToken]) -> None:
        """Deals with the logic for when the token is a LABEL type"""
        self._interpreter.add_label(line[0].value(), self.line_count())

    def on_read_input(self, var_name: str, value) -> None:
        """Deals with the logic for when the token is a READ type"""
        pseudo_input = [f'LET {var_name} {value}']
        self.on_let(list(parsing.parse(pseudo_input))[0])

    def on_gosub(self, line: list[GrinToken], line_index: int) -> None:
        """Deals with the logic for when the token is a GO-SUB type"""
        self._interpreter.add_gosub(line_index)
        self.on_goto(line)

    def on_return(self) -> None:
        """Deals with the logic for when the token is a RETURN type"""
        if len(self._interpreter.gosub_stack()) < 1: return
        self._line_count = self._interpreter.gosub_stack().pop(-1)

    def interpret_line(self, line: list[GrinToken]) -> None:
        first_command = line[_FIRST_COMMAND]
        match first_command.kind():
            case t.GrinTokenKind.DOT | t.GrinTokenKind.END:
                self._running = False
                self.end_program()
            case t.GrinTokenKind.LET:
                self.on_let(line)
            case t.GrinTokenKind.PRINT:
                self.on_print(line)
            case t.GrinTokenKind.ADD:
                self.on_arithmetic(line, lambda first_value, second_value: first_value + second_value)
            case t.GrinTokenKind.SUB:
                self.on_arithmetic(line, lambda first_value, second_value: first_value - second_value)
            case t.GrinTokenKind.DIV:
                self.on_arithmetic(line, lambda first_value, second_value: first_value / second_value)
            case t.GrinTokenKind.MULT:
                self.on_arithmetic(line, lambda first_value, second_value: first_value * second_value)
            case t.GrinTokenKind.GOTO:
                self.on_goto(line)
            case t.GrinTokenKind.IDENTIFIER: # this one is for flags
                if self._interpreter.get_label(line[0].value()): self.interpret_line(line[2:])
                self.on_label(line)
            case t.GrinTokenKind.GOSUB:
                self.on_gosub(line, self.line_count())
            case t.GrinTokenKind.INNUM:
                try:
                    user_input = int(input())
                except ValueError:
                    self.end_program("ValueError: Cannot interpret number")
                else:
                    self.on_read_input(line[1].value(), user_input)
            case t.GrinTokenKind.INSTR:
                user_input = '"' + input() + '"'
                self.on_read_input(line[1].value(), user_input)
            case t.GrinTokenKind.RETURN:
                self.on_return()
            case _:
                self.end_program("Unknown token type")

    @staticmethod
    def end_program(message:str = "") -> None:
        print(message)
        # REMEMBER TO PLACE THE sys.exit()

    def send_input(self, input_lines: list[str]) -> None:
        try:
            code_lines = list()

            for lines in parsing.parse(input_lines):
                if lines[0].kind() == t.GrinTokenKind.IDENTIFIER and lines[1].kind() == t.GrinTokenKind.COLON:
                    self._interpreter.add_label(lines[0].value(), self._temp_index)
                    code_lines.append(lines[2:])
                else: code_lines.append(lines)
                self._temp_index += 1

            while self._line_count < len(code_lines):
                if not self._running: return
                self.interpret_line(code_lines[self._line_count])
                self._line_count += 1
        except GrinParseError as e:
            self.end_program(e.__str__())

