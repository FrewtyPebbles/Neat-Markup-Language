


def TokenErr(err_type:str, l_n, c_n, extra = "") -> str:
	description = ""
	if err_type == "invalid_num":
		description = "The number format you used is invalid."
	elif err_type == "index_conflict":
		description = f"You are attempting to overwrite the same index '{c_n}' (X) more than once in the section \"{l_n}\" (Y)."
	elif err_type == "dict_literal":
		description = f"You are attempting to insert a literal '{c_n}' into a dictionary"
	elif err_type == "module_path_nonexistant":
		description = f"You are attempting import a module at a file path ({extra}) that does not exist."

	return f"  - NEAT < [{err_type}] Y({l_n}) X({c_n}) > {description}"