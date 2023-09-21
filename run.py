from kernel.utils import Shell

if __name__ == '__main__':
    shell = Shell('', 'G:/My Drive/Files To Backup/Python Projects/ShnozOS/centrl/data.json',
                  'G:/My Drive/Files To Backup/Python Projects/ShnozOS/call.json')
    while True:
        shell.execute()
