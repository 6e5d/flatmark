def csv2md(lines):
	result = []
	first_row = True
	for line in lines:
		lout = ""
		sp = line.split(",")
		first_col = True
		for word in sp:
			if first_col:
				lout += word
				first_col = False
			else:
				lout += f" | {word}"
		result.append(lout)
		if first_row:
			result.append(" | ".join(["---" for _ in sp]))
			first_row = False
	return "\n".join(result)
