import syncthing.cmd_add as cmd_add
import syncthing.cmd_init as cmd_init
import syncthing.cmd_pull as cmd_pull
import syncthing.cmd_pull_index as cmd_pull_index
import syncthing.cmd_push as cmd_push
import syncthing.cmd_push_index as cmd_push_index
import syncthing.cmd_status as cmd_status
import sys

commands = {
    'init': cmd_init,
    'status': cmd_status,
    'add': cmd_add,
    'push': cmd_push,
    'push_index': cmd_push_index,
    'pull': cmd_pull,
    'pull_index': cmd_pull_index,
}

def main():
    argv = sys.argv
    commands[argv[1]].run(argv[2:])
