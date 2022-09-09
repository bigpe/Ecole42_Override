import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect, exec_in_stream, exec_stream
from utils.text import print_output, print_title, print_magic
from utils.base import save_token, address_to_decimal

client = connect('level00', 'level00')

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'echo "test" | ./{binary_name}', title='Simple execute binary')
print_title('Okay, stdin intercepted, stdin write expected')
print_title('Send test in stdin')
print_output(output)
print_title('So sad! Obtain password?')
print_magic('Debug Time!')

func_info = exec(client, f'echo "info func" | gdb ./{binary_name} -q | egrep "main"', title='Get all functions')
print_output(func_info)
print_title('We have entry point (0x08048494 - main)')

main_structure = exec(client, f'echo "disass main" | gdb ./{binary_name} -q | egrep "cmp"', title='Get main structure')
print_output(main_structure)
print_title(f'We have CMP function, compare input with 0x149c, transform this')
password = str(address_to_decimal(0x149c))
print_title(f'Our password is {password}?')
print_title('Gotcha! Try this!')

output = exec(
    client,
    f'echo "\n" | (echo {password}; cat -) | ./{binary_name}',
    title='Execute binary again with obtained password'
)
print_output(output)
print_title('Access granted, done')
print_title('Check which user in use at now')

output = exec(
    client,
    f'echo "whoami" | (echo {password}; cat -) | ./{binary_name}',
    title='Execute binary again with obtained password'
)
user = output[0]
print_output(user)
print_title("Level01 - it's what we need, right?")

output = exec(
    client,
    f'echo "cat /home/users/{user}/.pass" | (echo {password}; cat -) | ./{binary_name}',
    title='Steal password'
)
token = output[0]
print_output(token)
print_title('Woo-hoo!')

save_token(token, client)

