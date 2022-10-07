from .datastructures.token.error import TokenErr
from .datastructures.token.character import WRAP
from .datastructures.token.complex import PTOK, ConfigSectionTitle
from .treecompiler import compiletree

def load(content: str):
	#the file is tokenized into a token list
	token_list = []
	string_buffer = ""
	wrapping = WRAP.NONE
	last_char = ""
	in_list = 0
	for (line_num, raw_line) in enumerate(content.splitlines()):
		line = raw_line.rstrip().lstrip() + " "
		if line == "[-] ": # END_SEC dont create an END_L
			token_list.append(PTOK.END_SEC)
		elif line == "~ ": # END_SEC dont create an END_L
			token_list.append(PTOK.E_LIST)
			in_list = 0
		else:
			for col_num, curr_char in enumerate(line):
				if wrapping == WRAP.Q_SING and curr_char != "'":
					string_buffer += curr_char
				elif wrapping == WRAP.Q_DOUB and curr_char != '"':
					string_buffer += curr_char
				elif wrapping == WRAP.SECT and curr_char != "]":
					string_buffer += curr_char
				if wrapping == WRAP.NONE:
					if curr_char == '"':
						string_buffer = ""
						wrapping = WRAP.Q_DOUB
					elif curr_char == "'":
						string_buffer = ""
						wrapping = WRAP.Q_SING
					elif curr_char == "[":
						wrapping = WRAP.SECT
					elif curr_char == "(":
						in_list += 1
						token_list.append(PTOK.S_LIST)
					elif curr_char == ")" and not last_char.isdigit():
						in_list -= 1
						token_list.append(PTOK.E_LIST)
					elif curr_char == "-" and col_num == 0 and in_list == 0:
						token_list.append(PTOK.AUTO_IND)
					elif (curr_char.isspace() or curr_char in (":",",",")")) and string_buffer not in ("","-"):
						try:
							if "." in string_buffer:
								num = float(string_buffer)
								token_list.append(num)
							else:
								num = int(string_buffer)
								token_list.append(num)
						except:
							try:
								num = int(string_buffer)
								token_list.append(num)
							except:
								print(TokenErr("invalid_num", line_num + 1, col_num))
								return False
						if curr_char == ")":
							token_list.append(PTOK.E_LIST)
							in_list -= 1
						string_buffer = ""
					elif curr_char == "-" or curr_char == "." or curr_char.isdigit():
						string_buffer += curr_char
				elif curr_char == '"' and wrapping == WRAP.Q_DOUB:
					token_list.append(string_buffer)
					string_buffer = ""
					wrapping = WRAP.NONE
				elif curr_char == "'" and wrapping == WRAP.Q_SING:
					token_list.append(string_buffer)
					string_buffer = ""
					wrapping = WRAP.NONE
				elif curr_char == ']' and wrapping == WRAP.SECT:
					token_list.append(ConfigSectionTitle(string_buffer))
					string_buffer = ""
					wrapping = WRAP.NONE
				last_char = curr_char
		if line != "" and wrapping == WRAP.NONE and not line.endswith("[-] ") and in_list == 0:
			if line.endswith(": "):
				in_list += 1
				token_list.append(PTOK.S_LIST)
			else:
				token_list.append(PTOK.END_L)
	#print(token_list)
	return compiletree(token_list)