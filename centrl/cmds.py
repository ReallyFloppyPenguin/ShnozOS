from tools.error import ShellInstanceError, FATAL_ERR, SHELL, \
IS_NOT, OF_TYPE, ERROR, QUOTE, INVALID_ENV_VAR, MISSING_ARG, FILE_EXISTS#, \

from hashlib import sha256
from .version import *
from subprocess import Popen, PIPE
from os import mkdir, remove

cmds = [
    'cd', 'rsetu', 'quit', 'udateu', 'github', 'ver', 'setenv', 'mkenv',
    'dlenv', 'help', 'wincmd', 'arth', 'new', 'edit'
]

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
    if instance.json:
        try:
            env_var_name = cmd_set_seq[1]
            val = cmd_set_seq[2]
            d = instance.json
            try:
                if instance.json['env'][env_var_name]:
                    d['env'][env_var_name] = val
                    instance.dump(d, 'centrl/data.json')
            except KeyError:
                print(ERROR, INVALID_ENV_VAR, QUOTE+env_var_name+QUOTE)
        except IndexError:
            print(ERROR, 'No environment variable name and value not defined')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def mkenv(cmd_set_seq, instance):
    if instance.json:
        try:
            try:
                env_var_name = cmd_set_seq[1]
                val = cmd_set_seq[2]
                d = instance.json
                d['env'][env_var_name] = val
            except KeyError:
                d['env'] = {}
                env_var_name = cmd_set_seq[1]
                val = cmd_set_seq[2]
                d = instance.json
                d['env'][env_var_name] = val
            instance.dump(d, 'centrl/data.json')
        except IndexError:
            print(ERROR, 'No environment variable name and value not defined')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def dlenv(cmd_set_seq, instance):
    if instance.json:
        d = instance.json
        ensure_password_is_right(instance)
        try:
            try:
                env_var_name = cmd_set_seq[1]
                del d['env'][env_var_name]
            except KeyError:
                d['env'] = {}
                env_var_name = cmd_set_seq[1]
                del d['env'][env_var_name]
            instance.dump(d, 'centrl/data.json')
        except IndexError:
            print(ERROR, 'No environment variable name and value not defined')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)

def wincmd(cmd_set_seq, instance):
    try:
        if cmd_set_seq[1]:
            pp = Popen(cmd_set_seq[1], stderr=PIPE, stdout=PIPE)
            pp.wait()
            out, err = pp.communicate()
            if not out and err:
                print(err)
            elif out and not err:
                print(out)
            else:
                print('cmd ended with outcode 0')
    except IndexError:
        print(ERROR, MISSING_ARG, '1.', 'Cannot run wincmd')


def new(cmd_set_seq, instance):
    if instance.cd:
        try:
            p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
            try:
                with open(p, 'x') as tempf:
                    pass
            except FileExistsError:
                print(ERROR, MISSING_ARG, '1.', 'Cannot run new')
        except IndexError:
            print(ERROR, FILE_EXISTS, p, 'Cannot create new file')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def dlete(cmd_set_seq, instance):
    if instance.cd:
        try:
            p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
            remove(p)
        except IndexError:
            print(ERROR, MISSING_ARG, '1.', 'Cannot run dlete')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def help(cmd_set_seq, instance):
    if cmd_set_seq[1] in cmds:
        print('Find help here:', github_link+'/wiki/'+'Commands/')


def arth(cmd_set_seq, instance):
    try:
        if cmd_set_seq[2] == '+':
            print(int(cmd_set_seq[1])+int(cmd_set_seq[3]))
    except Exception as e:
        print(e)



def ensure_password_is_right(instance):
    json = instance.json
    getting_password = True
    while getting_password:
        pss = input('Password: ')
        if not sha256(pss.encode()).hexdigest() == json['user']['password']:
            print('Wrong password')
            continue
        else:
            getting_password = False