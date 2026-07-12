from enum import Enum, auto
from exceptions import LexerException


class TokenType(Enum):
    """A collection of the different types of tokens."""

    # Literals
    IDENTIFIER = auto()
    NUMBER = auto()

    # Keywords
    LET = auto()
    INFINITY = auto()
    PI = auto()
    EULER = auto()

    # Delimiters
    L_PAREN = auto()
    R_PAREN = auto()
    COMMA = auto()

    # Operators
    COLON_EQUALS = auto()
    EQUALS = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    CARAT = auto()


class Token:
    """A representation of an individual token."""

    def __init__(self, type: TokenType, text: str, value: object):
        self.type = type
        self.text = text
        self.value = value

    def __repr__(self):
        if self.type in [TokenType.IDENTIFIER, TokenType.NUMBER]:
            return f"({self.type.name}: {self.text})"
        else:
            return f"({self.type.name})"


class Lexer:
    """A scanner that tokenizes user input."""
    
    TOKEN_SYMBOLS = {
        '(': "L_PAREN",
        ')': "R_PAREN",
        ',': "COMMA",
        '=': "EQUALS",
        '+': "PLUS",
        '-': "MINUS",
        '*': "STAR",
        '/': "SLASH",
        '^': "CARAT"
    }
    _keywords = {
        "let": TokenType.LET,
        "infinity": TokenType.INFINITY,
        "PI": TokenType.PI,
        "EULER": TokenType.EULER        
    }

    def __init__(self, user_input):
        # Text to be lexed
        self._user_input = user_input

        # List of tokens
        self._tokens = []

        # Position indices
        self._start_of_lexeme = 0
        self._current_index = 0

    def scanTokens(self) -> list[Token]:
        """Scan user input to create a list of tokens."""
        while not self._isFinished():
            self._start_of_lexeme = self._current_index
            self._scanToken()
        return self._tokens

    def _scanToken(self) -> None:
        """Scan for an individual token."""
        char = self._advance()

        # Single character tokens
        if char in TOKEN_SYMBOLS:
            self._addToken(TokenType[TOKEN_SYMBOLS[char]])

        # Two character token
        elif char == ":":
            if self._peek() == "=":
                self._advance()
                self._addToken(TokenType.COLON_EQUALS)

        # Multi character tokens
        elif char.isalpha() or char == "_":
            self._getText()
        elif char.isdigit():
            self._getNumber()

        # Whitespace
        elif char in [" ", "\t"]:
            pass

        # Unrecognized token
        else:
            column = self._current_index + 1
            raise LexerException(f'Unrecognized character at column {column}: "{char}".')

    def _getText(self) -> None:
        """Get text-based tokens, namely, identifiers and keywords."""
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self._user_input[self._start_of_lexeme : self._current_index]

        # Decide if text is a keyword or an identifier
        if text in self._keywords.keys():
            type = self._keywords[text]
            self._addToken(type)
        else:
            self._addToken(TokenType.IDENTIFIER, text)

    def _getNumber(self) -> None:
        """Get number tokens."""
        while self._peek().isdigit() or (self._peek() == "." and self._nextPeek().isdigit()):
            self._advance()

        number = float(self._user_input[self._start_of_lexeme : self._current_index])
        self._addToken(TokenType.NUMBER, number)

    def _advance(self) -> str:
        """Read the current character, then advance the index."""
        char = self._user_input[self._current_index]
        self._current_index += 1
        return char

    def _peek(self) -> str:
        """Read the next character from user input without advancing the index."""
        if self._isFinished():
            return "\0"
        else:
            # We can just look at _current_index because _advance() already pushes it by 1. 
            return self._user_input[self._current_index] 

    def _nextPeek(self) -> str:
        """Read the character after the next character without advancing the index."""
        if self._current_index + 1 >= len(self._user_input):
            return "\0"
        else:
            return self._user_input[self._current_index + 1]

    def _addToken(self, type: TokenType, value: object = None) -> None:
        """Add a token to the list of stored tokens."""
        text = self._user_input[self._start_of_lexeme : self._current_index]
        token = Token(type, text, value)
        self._tokens.append(token)

    def _isFinished(self) -> bool:
        """Check if lexing is complete."""
        return self._current_index >= len(self._user_input)


if __name__ == "__main__":
    user_input1 = "let f(x) := 9x^2 + sqrt( 1 - (cos(x/2))^2 )"
    user_input2 = "let equation_of_interest := ln(PI*x)"
    lexer = Lexer(user_input2)
    tokens = lexer.scanTokens()
    print(tokens)
