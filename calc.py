# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS','EOF'
OP_ADDITION, OP_SUBTRACTION = 'ADDITION', 'SUBTRACTION'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS or EOF
        self.type = type
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """
        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input!')

    def get_next_token(self):
        """Scanner

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more input to process
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to integer, create an INTEGER token,
        # go in a loop, incrementing self.pos and acquiring all the digits of the integer
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = None  # temporarily
            while current_char.isdigit():
                token = Token(INTEGER, int(current_char))
                self.pos += 1

                if self.pos == len(text):
                    break

                current_char += text[self.pos]

            return token

        elif current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        elif current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        elif current_char == ' ':
            # we skip whitespaces
            self.pos += 1
            return self.get_next_token()

        self.error()

    def validate_and_advance_token(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def ar_expr(self):
        """ar_expr -> INTEGER PLUS INTEGER
            Interprets the arithmetic expression and returns a result
        """
        operation = OP_ADDITION
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.validate_and_advance_token(INTEGER)  # validate_and_advance_token compares the current token with the expected token and goes to the next one if valid

        # we expect the current token to be a '+' token
        op = self.current_token
        try:
            self.validate_and_advance_token(PLUS)
        except:
            # if it throws an error, it means we've been given a subtraction operatior
            self.validate_and_advance_token(MINUS)
            operation = OP_SUBTRACTION

        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.validate_and_advance_token(INTEGER)
        # after the above call the self.current_token is set to
        # EOF token

        if operation == OP_ADDITION:
            result = left.value + right.value
        else:  # operation == OP_SUBTRACTION
            result = left.value - right.value

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.ar_expr()
        print(result)


if __name__ == '__main__':
    main()