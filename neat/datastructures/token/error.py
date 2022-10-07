


def TokenErr(err_type:str, l_n, c_n) -> str:
	description = ""
	if err_type == "invalid_num":
		description = "The number format you used is invalid."
	elif err_type == "index_conflict":
			description = f"You are attempting to overwrite the same index '{c_n}' (X) more than once in the section \"{l_n}\" (Y)."

	return f"  - NEAT < [{err_type}] Y({l_n}) X({c_n}) > {description}"