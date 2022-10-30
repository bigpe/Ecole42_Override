import os

VM_ADDRESS = os.popen("prlctl list -f | grep 'Override' | awk '{print $3}'").readline().replace('\n', '')
if not VM_ADDRESS:
    VM_ADDRESS = '0.0.0.0'
VM_PORT = 4242
