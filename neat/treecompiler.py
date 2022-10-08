from .datastructures.nodes import ConfigSection
from .datastructures.token.error import TokenErr
from .datastructures.token.complex import PTOK, ConfigSectionTitle


def compiletree(token_list: list, module_dict:dict, filepath = "?"):
	#print(module_dict)
	global_dict = module_dict
	tree_stack = [global_dict]
	val_stack = [[]]
	il_key_stack = []
	sec_stack = ["GLOBAL"]
	nested_sec = []
	key = ""
	last_number_stack = [-1]
	last_node = ""
	curr_wrapper = PTOK.NONE
	appended_sec = False
	in_list = 0
	for token in token_list:
		if type(token) == ConfigSectionTitle:
			if appended_sec == False:
				nested_sec.append([])
				appended_sec = True
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
						print(TokenErr("index_conflict", sec_stack[len(sec_stack)-1], token.title, filepath=filepath))
						return False
			except:
				try:
					num = int(token.title)
					sec_stack.append(num)
					nested_sec[len(nested_sec)-1].append(num)
				except:
					sec_stack.append(token.title)
					nested_sec[len(nested_sec)-1].append(token.title)
					#print(nested_sec)
		if type(token) == PTOK:
			if token == PTOK.END_SEC:
				
				#if len(nested_sec[len(nested_sec)-1]) > 1:
				curr_sec = tree_stack[len(tree_stack)-2]
				for sec_ind, sec in enumerate(nested_sec[len(nested_sec)-1]):
					if sec not in curr_sec.keys():
						continue
					curr_sec = curr_sec[sec]
				
				try:
					curr_sec[nested_sec[len(nested_sec)-1][len(nested_sec[len(nested_sec)-1])-1]] = tree_stack[len(tree_stack)-1]
				except:
					tree_stack[len(tree_stack)-2][sec_stack[len(sec_stack)-1]
											  ] = tree_stack[len(tree_stack)-1]
				tree_stack.pop()
				sec_stack.pop()
				nested_sec.pop()
				last_number_stack.pop()
			elif token == PTOK.END_L:
				if len(val_stack[0]) == 1:
					tree_stack[len(tree_stack)-1][key] = val_stack[0][0]
				elif len(val_stack[0]) > 1:
					if in_list:
						tree_stack[len(tree_stack)-1][key] = val_stack[0]
					else:# inline autoincrement
						for i, val in enumerate(val_stack[0]):
							if i > 0:
								last_number_stack[len(last_number_stack)-1] += 1
							tree_stack[len(tree_stack)-1][last_number_stack[len(last_number_stack)-1]] = val
				val_stack = [[]]
				key = ""
				if type(last_node) == ConfigSectionTitle:
					appended_sec = False
					tree_stack.append({})
					last_number_stack.append(-1)
			elif token == PTOK.AUTO_IND:
				last_number_stack[len(last_number_stack)-1] += 1
				key = last_number_stack[len(last_number_stack)-1]
			elif token == PTOK.S_LIST: #start list
				in_list += 1
				val_stack.append([])
			elif token == PTOK.E_LIST: #end list
				in_list -= 1
				if type(val_stack[len(val_stack)-2]) == dict:
					#print(il_key_stack)
					if len(il_key_stack) > 0:
						val_stack[len(val_stack)-2][il_key_stack[len(il_key_stack)-1]] = val_stack[len(val_stack)-1]
						val_stack.pop()
						il_key_stack.pop()
				elif type(val_stack[len(val_stack)-2]) == list:
					val_stack[len(val_stack)-2].append(val_stack[len(val_stack)-1])
					val_stack.pop()
			elif token == PTOK.IL_S_DICT:
				val_stack.append({})
			elif token == PTOK.IL_E_DICT:
				#print(il_key_stack)
				if type(val_stack[len(val_stack)-2]) == dict:
					if len(il_key_stack) > 0:
						val_stack[len(val_stack)-2][il_key_stack[len(il_key_stack)-1]] = val_stack[len(val_stack)-1]
						val_stack.pop()
						il_key_stack.pop()
				elif type(val_stack[len(val_stack)-2]) == list:
					val_stack[len(val_stack)-2].append(val_stack[len(val_stack)-1])
					val_stack.pop()
			elif token == PTOK.IL_DICT:
				if in_list:
					il_key_stack.append(last_node)
		elif type(token) in (str, bool) or token is None:
			if key == "":
				key = token
			else:
				if type(val_stack[len(val_stack)-1]) == list:
					val_stack[len(val_stack)-1].append(token)
				elif type(val_stack[len(val_stack)-1]) == dict and last_node == PTOK.IL_DICT:
					if len(il_key_stack) > 0:
						val_stack[len(val_stack)-1][il_key_stack[len(il_key_stack)-1]] = token
						il_key_stack.pop()
				elif type(last_node) in (str, bool) or token is None:
					print(TokenErr("dict_literal", sec_stack[len(sec_stack)-1], token, filepath=filepath))
					return False
		elif type(token) in (float, int):
			if key == "":
				key = token
				if type(token) == int:
					if token not in val_stack[len(val_stack)-1] and token > last_number_stack[len(last_number_stack)-1]:
							last_number_stack[len(last_number_stack)-1] = token
					else:
						print(TokenErr("index_conflict", sec_stack[len(sec_stack)-1], token, filepath=filepath))
						return False
			else:
				if type(val_stack[len(val_stack)-1]) == list:
					val_stack[len(val_stack)-1].append(token)
				elif type(val_stack[len(val_stack)-1]) == dict and last_node == PTOK.IL_DICT:
					if len(il_key_stack) > 0:
						val_stack[len(val_stack)-1][il_key_stack[len(il_key_stack)-1]] = token
						il_key_stack.pop()
				elif type(token) in (float, int):
					print(TokenErr("dict_literal", sec_stack[len(sec_stack)-1], token, filepath=filepath))
					return False
		last_node = token
	#print(global_dict)
	return global_dict
