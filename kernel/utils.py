from hashlib import sha256
from json import load as l, dump as d
from tools.parser import Parse
from centrl.cmds import *
from tools.error import ERROR, INVALID_CMD, QUOTE

class Shell:
    def __init__(self, fsf: str, data_j: str) -> None:
        self.cd = 'root'
        self.json = self.load('centrl/data.json')
        try:
            if not self.json['user']['username']:
                self.create_user()
        except AttributeError:
            self.create_user()
        self.username = self.json['user']['username']
        self.passw = self.json['user']['password']
        self.inp_start = f'{self.username}@{self.cd}$ '
        self.jp = data_j.encode('utf-8')
        self.fsf = fsf
            
        
    def create_user(self):
        print('Please fill this form to create a user')
    

        username = input('Username: ')
        passw = input('Password (it will be hashed): ')
        data_to_dump = {
            'user': {
                'username': username,
                'password': sha256(passw.encode('utf-8')).hexdigest()
            }
        }
        self.dump(data_to_dump, 'centrl/data.json')
        self.json = self.load('centrl/data.json')


    def execute(self):
        while True:
            inp = input(self.inp_start)
            self.handle(inp)


    def handle(self, inp):
        cmd_set_seq = Parse().parse(inp)
        if cmd_set_seq[0] == 'cd':
            # Use the cd func from centrl
            c_d = cd(cmd_set_seq, self)
            self.reload(c_d)

        if cmd_set_seq[0] == 'rsetu':
            rsetu(cmd_set_seq, self)

        if cmd_set_seq[0] == 'udateu':
            udateu(cmd_set_seq, self)

        if cmd_set_seq[0] == 'quit':
            quit()

        if cmd_set_seq[0] == 'ver':
            ver(cmd_set_seq, self)

        if cmd_set_seq[0] == 'github':
            github(cmd_set_seq, self)

        if cmd_set_seq[0] == 'help':
            help(cmd_set_seq, self)

        if cmd_set_seq[0] == 'setenv':
            setenv(cmd_set_seq, self)

        if cmd_set_seq[0] == 'mkenv':
            mkenv(cmd_set_seq, self)

        if cmd_set_seq[0] == 'dlenv':
            dlenv(cmd_set_seq, self)

        if not cmd_set_seq[0] in cmds:
            # Cmd not listed so create error
            print(ERROR, INVALID_CMD, QUOTE+cmd_set_seq[0]+QUOTE, 3)

        self.reload(self.cd)


    def load(self, path):
        with open(path, 'r') as tempf:
            data = l(tempf)
            tempf.close()

        return data

    
    def dump(self, data, path):
        with open(path, 'w') as tempf:
            d(data, tempf)
            tempf.close()


    def reload(self, cd):
        self.cd = cd
        self.json = self.load('centrl/data.json')
        try:
            if not self.json['user']['username']:
                self.create_user()
        except KeyError:
            self.create_user()
        self.username = self.json['user']['username']
        self.passw = self.json['user']['password']
        self.inp_start = f'{self.username}@{self.cd}$ '