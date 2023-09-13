class Multimedia:
	def __init__(self, url, ty):
		self.url = url
		self.ty = ty

class Code:
	def __init__(self, lines, prefix):
		self.lines = lines
		self.prefix = prefix
	def __repr__(self):
		result = f"```{self.prefix}\n"
		result += "\n".join(self.lines)
		result += "\n```"
		return result

class Paragraph:
	def __init__(self, data):
		self.data = data
	def __repr__(self):
		return self.data

class Title:
	def __init__(self, title):
		self.data = title
	def __repr__(self):
		return f"# {self.data}"

class Section:
	def __init__(self, blocks):
		assert isinstance(blocks[0], Title)
		self.title = blocks[0]
		self.blocks = blocks[1:]
	def __repr__(self):
		result = "===BEGIN OF SECTION===\n"
		result += str(self.title) + "\n\n"
		for block in self.blocks:
			result += str(block) + "\n\n"
		result += "===END OF SECTION===\n"
		return result

def lines2blocks(lines):
	blocks = []
	assert isinstance(lines, list)
	tmp_block = []
	for line in lines:
		assert isinstance(line, str)
		line = line.rstrip()
		if not line:
			if tmp_block:
				blocks.append(tmp_block)
			tmp_block = []
			continue
		tmp_block.append(line)
	if tmp_block:
		blocks.append(tmp_block)
	return blocks

def parse_block(block):
	if block[0].startswith("# "):
		s = " ".join(block)
		s = s.removeprefix("# ")
		return Title(s)
	if block[0].startswith("<"):
		s = "".join(block)
		assert s.endswith(">")
		s = s.removeprefix("<")
		s = s.removesuffix(">")
		sp = s.rsplit(".", 1)
		if len(sp) == 2:
			if sp[1] in ["png", "jpg", "gif"]:
				return Multimedia(s, "image")
			if sp[1] in ["opus", "flac", "wav"]:
				return Multimedia(s, "audio")
	if block[0].startswith("```"):
		assert block[-1].startswith("```")
		prefix = block[0].removeprefix("```")
		return Code(block[1:-1], prefix.strip())
	s = " ".join([line.strip() for line in block])
	return Paragraph(s)

class Document:
	def __init__(self, lines):
		self.sects = []
		blocks = lines2blocks(lines)
		tmp_blocks = []
		for block in blocks:
			if block[0][0] == "#":
				if tmp_blocks:
					self.sects.append(Section(tmp_blocks))
					tmp_blocks = []
			tmp_blocks.append(parse_block(block))
		if tmp_blocks:
			self.sects.append(Section(tmp_blocks))

	def __repr__(self):
		result = ""
		for sect in self.sects:
			result += str(sect)
		return result
