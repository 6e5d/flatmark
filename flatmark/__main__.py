import sys
from flatmark.conv_md import conv_md_file
from .flatmark import Document

if __name__ == "__main__":
	lines = conv_md_file(sys.argv[1])
	print(end = "\n".join(lines))
