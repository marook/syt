#!/bin/bash
set -e

export syt=`realpath ../syt.py`

step(){
    echo ''
    echo '---------------------------------------'
    echo "  $1"
}

step 'Cleanup'
if [[ -e 'repo' ]]
then
    rm -rf 'repo'
fi
if [[ -e 'remote' ]]
then
    rm -rf 'remote'
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

step 'init remote'
mkdir 'remote'
${syt} init 'remote'

step 'push world.txt to remote'
( cd 'repo' && ${syt} push '../remote' 'world.txt' )

step 'status remote'
( cd 'repo' && ${syt} status )

step 'pull pull.txt from remote'
echo 'something else' > 'remote/pull.txt'
( cd 'remote' && ${syt} add 'pull.txt' )
( cd 'repo' && ${syt} pull '../remote' 'pull.txt' )

step 'status'
( cd 'repo' && ${syt} status )

step 'push index'
( cd 'repo' && ${syt} push_index '../remote' )

step 'pull index'
( cd 'repo' && ${syt} pull_index '../remote' )

step 'pull everything from remote'
echo 'something new' > 'remote/pull_all.txt'
( cd 'remote' && ${syt} add 'pull_all.txt' )
( cd 'repo' && ${syt} pull '../remote' )
