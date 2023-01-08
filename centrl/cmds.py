from tools.error import ShellInstanceError, FATAL_ERR, SHELL, IS_NOT, OF_TYPE
from hashlib import sha256

cmds = ['cd', 'rsetu', 'quit', 'udateu']

def cd(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.cd:
        return f'{cmd_set_seq[1]}'
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def rsetu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.json:
        d = instance.json
        del d['username']
        del d['password']
        instance.dump(d, 'centrl/data.json')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def udateu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    # TODO fix if user did not make any paramerters
    if instance.json:
        d = instance.json
        try:
            d['username'] = cmd_set_seq[1]
            d['password'] = sha256(cmd_set_seq[2].encode('utf-8')).hexdigest()
        except IndexError:
            d['username'] = input('Username: ')
            d['password'] = sha256(input('Password (it will be hashed): ').encode('utf-8')).hexdigest()
        instance.dump(d, 'centrl/data.json')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)