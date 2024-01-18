import sys
import time

# commands_that_need_block['\\section', '\\subsection', '\\subsubsection', '\\paragraphb', '\\par', '\\ac', '\\texttt', '\\textbf', '\\textit']
# commands_that_dont_need_block['\\label']
# commands_that_need_block_replaced['\\autoref', '\\secref', '\\cite']

def find_command(buf):
	ind_s = buf.find('\\')
	if ind_s == -1:
		return -1
	if buf[ind_s + 1:ind_s+4] == 'par':
		return ('\\par',(ind_s, ind_s+4))
	ind_e = buf.find('{', ind_s)
	return (buf[ind_s:ind_e], (ind_s, ind_e))

def remove_command(buf, indexes):
	buf = buf[:indexes[0]] + buf[indexes[1] + 1 :]
	buf = buf.replace('}','',1)
	return buf

def remove_command_and_block(buf, indexes):
	ind_e = buf.find('}')
	return buf[:indexes[0]] + buf[ind_e + 1 :]

def remove_command_replace_block(buf, indexes, replace_with):
	ind_e = buf.find('}')
	return buf[:indexes[0]]+ replace_with + buf[ind_e + 1 :]

if len(sys.argv) != 2:
	print("Exactly one argument needed! The Path to the input file.")

f = open(sys.argv[1], "r")
buf = f.read()
while 1:
	command = find_command(buf)
	if command == -1:
		break
	print(command[0])
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
		case '\\par':
			buf = remove_command(buf, command[1])
		case '\\ac':
			buf = remove_command(buf, command[1])
		case '\\texttt':
			buf = remove_command(buf, command[1])
		case '\\textbf':
			buf = remove_command(buf, command[1])
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
			ind_end_s = buf.find('\\end')
			ind_end_e = buf.find('}', ind_end_s, ind_end_s + 20)
			buf = buf[:command[1][0]] + buf[ind_end_e + 1:]
		case _:
			print("Found not handeled command:" + command[0])
			print(command)
			print("Please add and try again")
			print()
			print(buf)
			sys.exit()

print(buf)
