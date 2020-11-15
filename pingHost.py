import os
def host(host):
    response = os.system("ping  " + host)
    if response == 0:
        print('Host: ' + host + '\n' 'Status: ' + "True")
    else:
        print('Host: ' + host + '\n' 'Status: ' + "False")