from .datastructures.nodes import ConfigSection
from .datastructures.token.error import TokenErr
from .datastructures.token.complex import PTOK, ConfigSectionTitle


def compiletree(token_list: list):
	global_dict = {}
	tree_stack = [global_dict]
	val_stack = [[]]
	sec_stack = ["GLOBAL"]
	key = ""
	last_number_stack = [-1]
	curr_wrapper = PTOK.NONE
	for token in token_list:
		if type(token) == ConfigSectionTitle:
			try:
				if "." in token.title:
					num = float(token.title)
					sec_stack.append(num)
				else:
					num = int(token.title)
					if num not in tree_stack[len(tree_stack)-1].keys():
						if num > last_number_stack[len(last_number_stack)-1]:
							last_number_stack[len(last_number_stack)-1] = num
						sec_stack.append(num)
					else:
						print(TokenErr("index_conflict", sec_stack[len(sec_stack)-1], token.title))
						return False
			except:
				try:
					num = int(token.title)
					sec_stack.append(num)
				except:
					sec_stack.append(token.title)
			tree_stack.append({})
			last_number_stack.append(-1)
		if type(token) == PTOK:
			if token == PTOK.END_SEC:
				tree_stack[len(tree_stack)-2][sec_stack[len(sec_stack)-1]
											  ] = tree_stack[len(tree_stack)-1]
				tree_stack.pop()
				sec_stack.pop()
				last_number_stack.pop()
			elif token == PTOK.END_L:
				if len(val_stack[0]) == 1:
					tree_stack[len(tree_stack)-1][key] = val_stack[0][0]
				elif len(val_stack[0]) > 1:
					tree_stack[len(tree_stack)-1][key] = val_stack[0]
				val_stack = [[]]
				key = ""
			elif token == PTOK.AUTO_IND:
				last_number_stack[len(last_number_stack)-1] += 1
				key = last_number_stack[len(last_number_stack)-1]
			elif token == PTOK.S_LIST: #start list
				val_stack.append([])
			elif token == PTOK.E_LIST: #end list
				val_stack[len(val_stack)-2].append(val_stack[len(val_stack)-1])
				val_stack.pop()
		elif type(token) == str:
			if key == "":
				key = token
			else:
				val_stack[len(val_stack)-1].append(token)
		elif type(token) in [float, int]:
			if key == "":
				key = token
				if type(token) == int:
					if token not in val_stack[len(val_stack)-1]:
						if token > last_number_stack[len(last_number_stack)-1]:
							last_number_stack[len(last_number_stack)-1] = token
					else:
						print(TokenErr("index_conflict", sec_stack[len(sec_stack)-1], token))
						return False
			else:
				val_stack[len(val_stack)-1].append(token)
	#print(global_dict)
	return global_dict
