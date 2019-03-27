#!/bin/bash
set -e

export syt=`realpath ../syt.py`

step(){
    echo '---------------------------------------'
    echo "$1"
}

step 'Cleanup'
if [[ -e 'repo' ]]
then
    rm -rf 'repo'
fi

alias

step 'init'
mkdir 'repo'
${syt} init 'repo'

step 'status'
( cd 'repo' && ${syt} status )

step 'add'
echo 'hello world' > 'repo/world.txt'
( cd 'repo' && ${syt} add 'world.txt' )

step 'status'
( cd 'repo' && ${syt} status )
