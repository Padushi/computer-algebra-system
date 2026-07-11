from enum import Enum, auto
from exceptions import LexerException

class TokenType(Enum):
    """A collection of the different types of tokens."""

    # Literals
    IDENTIFIER = auto()
    NUMBER = auto()

    # Keywords
    INFINITY = auto()
    PI = auto()
    EULER = auto()

    # Delimiters
    L_PAREN = auto()
    R_PAREN = auto()
    COMMA = auto()

    # Operators
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

    _keywords = {
        "INFINITY": TokenType.INFINITY,
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

    def scanTokens(self):
        """Scan user input to create a list of tokens."""
        while not self._isFinished():
            self._start_of_lexeme = self._current_index
            self._scanToken()
        return self._tokens
    

    def _scanToken(self):
        """Scan for an individual token."""
        char = self._advance()

        if char == "(":
            self._addToken(TokenType.L_PAREN)
        elif char == ")":
            self._addToken(TokenType.R_PAREN)
        elif char == ",":
            self._addToken(TokenType.COMMA)
        elif char == "=":
            self._addToken(TokenType.EQUALS)
        elif char == "+":
            self._addToken(TokenType.PLUS)
        elif char == "-":
            self._addToken(TokenType.MINUS)
        elif char == "*":
            self._addToken(TokenType.STAR)
        elif char == "/":
            self._addToken(TokenType.SLASH)
        elif char == "^":
            self._addToken(TokenType.CARAT)
        elif char.isalpha():
            self._getText()
        elif char.isdigit():
            self._getNumber()
        elif char in [" ", "\t"]:
            pass
        else:
            column = self._current_index + 1
            raise LexerException(f"Unrecognized character at column {column}: \"{char}\".")          

        
    def _getText(self):
        """Get text-based tokens, namely, identifiers and keywords."""
        while self._peek().isalnum():
            self._advance()
            

        text = self._user_input[self._start_of_lexeme:self._current_index]

        # Decide if text is a keyword or an identifier
        if text in self._keywords.keys():
            type = self._keywords[text]
            self._addToken(type)
        else:
            self._addToken(TokenType.IDENTIFIER, text)

    
    def _getNumber(self):
        """Get number tokens."""
        while self._peek().isdigit() or (self._peek() == "." and self._nextPeek().isdigit()):
            self._advance()

        number = float(self._user_input[self._start_of_lexeme:self._current_index])
        self._addToken(TokenType.NUMBER, number)

    
    def _advance(self):
        """Read the current character, then advance the index."""
        char = self._user_input[self._current_index]
        self._current_index += 1 
        return char


    def _peek(self):
        """Read the next character from user input without advancing the index."""
        if self._isFinished():
            return "\0"
        else:
            return self._user_input[self._current_index]
        
    def _nextPeek(self):
        """Read the character after the next character without advancing the index."""
        if self._current_index + 1 >= len(self._user_input):
            return "\0"
        else:
            return self._user_input[self._current_index + 1]
        

    def _addToken(self, type: TokenType, value: object=None):
        """Add a token to the list of stored tokens."""
        text = self._user_input[self._start_of_lexeme:self._current_index]
        token = Token(type, text, value)
        self._tokens.append(token)


    def _isFinished(self):
        """Check if lexing is complete."""
        return self._current_index >= len(self._user_input)
    

if __name__ == "__main__":
    user_input = "flare1 = limit(x^5 + sin(35.2) + 9.0, INFINITY)"
    lexer = Lexer(user_input)
    tokens = lexer.scanTokens()
    print(tokens)