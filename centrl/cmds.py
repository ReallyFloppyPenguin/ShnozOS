from tools.error import ShellInstanceError, FATAL_ERR, SHELL, \
IS_NOT, OF_TYPE, ERROR, QUOTE, INVALID_ENV_VAR
from hashlib import sha256
from .version import *

cmds = ['cd', 'rsetu', 'quit', 'udateu', 'github', 'ver', 'setenv']

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
        del d['user']['username']
        del d['user']['password']
        instance.dump(d, 'centrl/data.json')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def udateu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    # TODO fix if user did not make any paramerters
    if instance.json:
        d = instance.json
        try:
            d['user']['username'] = cmd_set_seq[1]
            d['user']['password'] = sha256(cmd_set_seq[2].encode('utf-8')).hexdigest()
        except IndexError:
            d['user']['username'] = input('Username: ')
            d['user']['password'] = sha256(input('Password (it will be hashed): ').encode('utf-8')).hexdigest()
        instance.dump(d, 'centrl/data.json')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def ver(cmd_set_seq, instance):
    print(version)


def github(cmd_set_seq, instance):
    print(github_link)


def setenv(cmd_set_seq, instance):
    try:
        env_var_name = cmd_set_seq[1]
        val = cmd_set_seq[2]
        d = instance.json
        try:
            if instance.json['env'][env_var_name]:
                d['env'][env_var_name] = val
        except KeyError:
            print(ERROR, INVALID_ENV_VAR, QUOTE+env_var_name+QUOTE)
        if d.get(env_var_name):
            d['env'][env_var_name] = val
            instance.dump(d, 'centrl/data.json')
        else:
            print(ERROR, INVALID_ENV_VAR, QUOTE+env_var_name+QUOTE)
    except IndexError:
        print(ERROR, 'No environment variable name and value not defined')