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
import sys

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

def main():
    argv = sys.argv
    commands[argv[1]].run(argv[2:])
