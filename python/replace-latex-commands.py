import sys
import time
import re

STR_LEN_BEGIN = 6
# commands_that_need_block['\\section', '\\subsection', '\\subsubsection', '\\paragraphb', '\\par', '\\ac', '\\texttt', '\\textbf', '\\textit']
# commands_that_dont_need_block['\\label']
# commands_that_need_block_replaced['\\autoref', '\\secref', '\\cite']
chars_need_escaping = ['%', '$', '{', '}', '_', 'P', '#', '&', 'S']

def remove_all_escape_char(buf):
	ind = buf.find('\\')
	while ind != -1:
		if buf[ind + 1] in chars_need_escaping:
			buf = ''.join((buf[:ind], buf[ind + 1:]))
		else:
			ind = ind + 1
		ind = buf.find('\\', ind)
	return buf

def remove_all_inline_mathmode(buf):
	ind_s = buf.find('$')
	while ind_s != -1:
		ind_e = buf.find('$', ind_s + 1)
		buf = ''.join((buf[:ind_s], buf[ind_e + 1:]))
		ind_s = buf.find('$')
	return buf

def find_command(buf):
	ind_s = buf.find('\\')
	if ind_s == -1:
		return -1
	ind_w = re.search(r"\s", buf[ind_s:]).start() + ind_s
	ind_b = buf.find("{", ind_s)
	if ind_b != -1:
		ind_e = min(ind_b, ind_w)
	else:
		ind_e = ind_w
	return (buf[ind_s:ind_e], (ind_s, ind_e))

def remove_command_without_braces(buf, indexes):
	return ''.join((buf[:indexes[0]], buf[indexes[1] + 1 :]))

def remove_command(buf, indexes):
	buf = ''.join((buf[:indexes[0]], buf[indexes[1] + 1 :]))
	buf = buf.replace('}','',1)
	return buf

def remove_command_and_block(buf, indexes):
	ind_e = buf.find('}', indexes[1])
	return ''.join((buf[:indexes[0]], buf[ind_e + 1:]))

def remove_command_replace_block(buf, indexes, replace_with):
	ind_e = buf.find('}', indexes[0])
	return ''.join((buf[:indexes[0]], replace_with, buf[ind_e + 1:]))

def remove_begin_end_block(buf, indexes):
	ind_b = buf.find('\\begin', indexes[1])
	ind_end_s = buf.find('\\end', indexes[1])
	if ind_b != -1:
		while ind_b < ind_end_s:
			buf = remove_begin_end_block(buf, (ind_b, ind_b + STR_LEN_BEGIN))
			ind_b = buf.find('\\begin', indexes[1])
			ind_end_s = buf.find('\\end', indexes[1])
	ind_end_e = buf.find('}', ind_end_s)
	return ''.join((buf[:indexes[0]], buf[ind_end_e + 1:]))

def remove_inlinecode_command(buf, indexes):
	ind_e = buf.find('}', indexes[1])
	buf = ''.join((buf[:indexes[0]], buf[ind_e + 1:]))
	buf = buf.replace('{','',1)
	buf = buf.replace('}','',1)
	return buf

if len(sys.argv) != 2:
	print("Exactly one argument needed! The Path to the input file.")

f = open(sys.argv[1], "r")
buf = f.read()
if buf[-1] != "\n":
	buf = ''.join((buf,"\n"))

buf = remove_all_escape_char(buf)
buf = remove_all_inline_mathmode(buf)

while 1:
	command = find_command(buf)
	if command == -1:
		break
	print(command)
	match command[0]:
		case '\\section':
			buf = remove_command(buf, command[1])
		case '\\subsection':
			buf = remove_command(buf, command[1])
		case '\\subsubsection':
			buf = remove_command(buf, command[1])
		case '\\paragraphb':
			buf = remove_command(buf, command[1])
		case '\\paragraph':
			buf = remove_command(buf, command[1])
		case '\\ac':
			buf = remove_command(buf, command[1])
		case '\\texttt':
			buf = remove_command(buf, command[1])
		case '\\textbf':
			buf = remove_command(buf, command[1])
		case '\\textit':
			buf = remove_command(buf, command[1])
		case '\\inlinecode':
			buf = remove_inlinecode_command(buf, command[1])
		case '\\par':
			buf = remove_command_without_braces(buf, command[1])
		case '\\newline':
			buf = remove_command_without_braces(buf, command[1])
		case '\\label':
			buf = remove_command_and_block(buf, command[1])
		case '\\autoref':
			buf = remove_command_replace_block(buf, command[1], 'Figure 1')
		case '\\secref':
			buf = remove_command_replace_block(buf, command[1], 'Section 1')
		case '\\cite':
			buf = remove_command_replace_block(buf, command[1], '[1]')
		case '\\begin':
			print("found begin")
			buf = remove_begin_end_block(buf, command[1])
		case _:
			print("Found not handeled command:" + command[0])
			print(command)
			print("Please add and try again")
			print()
			print(buf)
			sys.exit()

print(buf)
