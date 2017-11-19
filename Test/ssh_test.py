from pexpect import pxssh
from utils import Utils

if __name__ == '__main__':
    s = pxssh.pxssh()
    u = Utils()
    print('Hostname: {}'.format(u.get_hostname()))
    print('Username: {}'.format(u.get_username()))
    print('Password: {}'.format(u.get_password()))
    if not s.login(u.get_hostname(),\
                   u.get_username(),\
                   u.get_password()):
        print('SSH session failed on login.')
        print(str(s))
    else:
        print('SSH session login successful')
        s.sendline ('ls -la')
        s.prompt()         # match the prompt
        print(s.before)     # print everything before the prompt.
        s.logout()