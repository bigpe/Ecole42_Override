import os

VM_ADDRESS = os.popen("prlctl list -f | grep 'Override' | awk '{print $3}'").readline().replace('\n', '')
VM_PORT = 4242
