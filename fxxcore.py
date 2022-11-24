# This file is a part of fuchsialang (fxx)
# (c) 2022 tomeczeklmaodev
# https://github.com/tomeczeklmaodev/fuchsialang/

# ---------------
# Constants
# ---------------

DIGITS = '0123456789'

# ---------------
# Errors
# ---------------

class Error:
	def __init__(self, pos_start, pos_end, err_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.err_name = err_name
		self.details = details

	def as_str(self):
		result = f'{self.err_name}: {self.details}\n' # ERROR NAME: ERROR DETAILS
		result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}' # File FILENAME, line LINENUMBER
		return result

class IllegalCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Illegar Character', details)

# ---------------
# Position
# ---------------

class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def advance(self, current_char):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# ---------------
# Tokens
# ---------------

TT_INTEGER  = 'INTEGER'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MULTIPLY = 'MULTIPLY'
TT_DIVIDE   = 'DIVIDE'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'

class Token:
	def __init__(self, type_, value=None):
		self.type = type_
		self.value = value

	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

# ---------------
# Lexer
# ---------------

class Lexer:
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def mk_tokens(self):
		tokens = []
		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.mk_number())
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MULTIPLY))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIVIDE))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN))
				self.advance()
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		return tokens, None

	def mk_number(self):
		num_str = ''
		dot_c = 0 # dot count, if dot_c is 1, then it is a float type, else integer

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_c == 1: break
				dot_c += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()

		if dot_c == 0:
			return Token(TT_INTEGER, int(num_str)) # return integer if number doesnt contain '.'
		else:
			return Token(TT_FLOAT, float(num_str)) # return float if number contains '.'

# ---------------
# Run
# ---------------

def run(fn, text):
	lexer = Lexer(fn, text)
	tokens, error = lexer.mk_tokens()

	return tokens, error
