
"""\
usage: %(program)s <command> [<arg>...]
Synchronize files the offline way.

commands:
%(commandhelp)s

Use '%(program)s <command> -h' for help on individual subcommand.
"""

import sys

from syncthing import (
        cmd_add,
        cmd_init,
        cmd_pull,
        cmd_pull_index,
        cmd_push,
        cmd_push_index,
        cmd_rm,
        cmd_status,
)

commands = {
    'init': cmd_init,
    'status': cmd_status,
    'add': cmd_add,
    'push': cmd_push,
    'push_index': cmd_push_index,
    'pull': cmd_pull,
    'pull_index': cmd_pull_index,
    'rm': cmd_rm,
}

commandhelp = '\n'.join((' ' * 3 + x for x in commands))
program = sys.argv[0]

def usage():
    sys.stderr.write(__doc__ % globals())

def main():
    argv = sys.argv
    if len(argv) < 2 or argv[1] not in commands:
        usage()
        sys.exit(1)

    commands[argv[1]].run(argv[2:])
    # commands should return a status; we have good faith for now.
    sys.exit(0)
