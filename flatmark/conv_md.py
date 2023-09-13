from .flatmark import Multimedia, Code, Document
from .csv2md import csv2md

def conv_md_block(block):
	if isinstance(block, Multimedia):
		match block.ty:
			case "image":
				return f"![]({block.url})"
			case "audio":
				return f'<audio controls src="{block.url}"></audio>'
			case x:
				raise Exception(x)
	elif isinstance(block, Code):
		if block.prefix == "csv":
			return csv2md(block.lines)
		else:
			return str(block)
	else:
		return str(block)

def conv_md(doc):
	result = []
	for sect in doc.sects:
		result.append(conv_md_block(sect.title))
		result.append("")
		for block in sect.blocks:
			result.append(conv_md_block(block))
			result.append("")
	return result

def conv_md_file(path):
	lines = [line for line in open(path)]
	doc = Document(lines)
	return conv_md(doc)
