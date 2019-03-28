#!/usr/bin/python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import cmd_add
import cmd_init
import cmd_pull
import cmd_pull_index
import cmd_push
import cmd_push_index
import cmd_status

commands = {
    'init': cmd_init,
    'status': cmd_status,
    'add': cmd_add,
    'push': cmd_push,
    'push_index': cmd_push_index,
    'pull': cmd_pull,
    'pull_index': cmd_pull_index,
}

def main(argv):
    commands[argv[1]].run(argv[2:])

if __name__ == '__main__':
    main(sys.argv)
