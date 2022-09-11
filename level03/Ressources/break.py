import os
import sys
import time

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, get_func_structure
from utils.text import print_output, print_title, print_magic, print_action
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
print_title("We need password, hurry!")
print_magic('Debug Time!')

func_info = exec(
    client,
    f'echo "info func" | gdb ./{binary_name} -q | egrep "main|decrypt|test"',
    title='Get all functions'
)
print_output(func_info)
print_title(
    'We have one entry point \n'
    '(0x08048660 - decrypt)'
    '(0x08048747 - test)'
    '(0x0804885a - main)'
)
print_title('Detailed view?')

main_structure = exec(
    client, f'echo "disass main" | gdb ./{binary_name} -q | egrep "103|112|123"',
    title='Get main structure'
)
print_output(main_structure)
print_title('Main read stdin and call test function with arg from stdin read and 0x1337d00d')
print_title('Maybe answer is 0x1337d00d?')

output = exec(client, 'printf "%d" 0x1337d00d')
print_output(output)
password = int(output[0])

output = exec(client, f'echo "{password}" | ./{binary_name}', title='I hope is our password, check it')
print_output(output)
print_title('It would be too easy')
print_magic('Another debug time...')

get_func_structure(client, 'test', filter=['+21>:', '+25>:', '+267>:'])
print_title('Compare our password with 0x15 (<= 21) difference from subtraction, and call decrypt function')
print_title('We can get into the decrypt function in 21 different ways, we can try everything')

for i in range(21):
    command = f'echo "{password}" | ./{binary_name} | grep "Invalid Password"'
    output = exec(client, command, silent=True)
    print(f'    Try - {password}', end='\r')
    time.sleep(.1)
    if not output:
        print_title('+ ')
        print_title('Password is found')
        print_action(command)
        break
    password -= 1
print_title('Time to dirty tricks!')

output = exec(
    client,
    f'echo "cat /home/users/level04/.pass" | (echo {password}; cat -) | ./{binary_name}',
    title='Steal password'
)
print_output(output)
print_title('Woo-hoo!')
token = output[0]

save_token(token)
