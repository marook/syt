#!/bin/bash
set -e

export syt=`realpath syt.py`

step(){
    echo ''
    echo '---------------------------------------'
    echo "  $1"
}

fail(){
    echo "ERROR $1" >&2
    exit 1
}

step 'Cleanup'
for repo in repo remote transfer
do
    if [[ -e "${repo}" ]]
    then
        rm -rf -- "${repo}"
    fi
done

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
( cd 'repo' && ${syt} pull '../remote' `realpath '../remote/pull.txt'` )
if [[ ! -e 'repo/pull.txt' ]]
then
    fail "pull.txt should have been pulled from remote"
fi

step 'status'
( cd 'repo' && ${syt} status --content-size )

step 'push index'
( cd 'repo' && ${syt} push_index '../remote' )

step 'pull index'
( cd 'repo' && ${syt} pull_index '../remote' )

step 'pull everything from remote'
echo 'something new' > 'remote/pull_all.txt'
( cd 'remote' && ${syt} add 'pull_all.txt' )
( cd 'repo' && ${syt} pull '../remote' )

step 'add and pull file in subdirectory'
mkdir 'remote/subdir'
echo 'hello world' > 'remote/subdir/peng.txt'
( cd 'remote' && ${syt} add 'subdir/peng.txt' )
( cd 'repo' && ${syt} pull '../remote' )

step 'push with content limit'
echo 'hello' > 'repo/neu.txt'
( cd 'repo' && ${syt} add 'neu.txt' )
( cd 'repo' && ${syt} push --limit-repo-content-size 1B '../remote' )
if [[ -e 'remote/neu.txt' ]]
then
    fail "neu.txt should not have been pushed because of content limit"
fi

step 'push with exclude repo content'
( cd 'repo' && ${syt} pull_index '../remote' )
mkdir 'transfer'
${syt} init 'transfer'
( cd 'repo' && ${syt} push '../transfer' --exclude-repo-content `realpath '../remote'` )

step 'pull index by name'
( cd 'transfer' && ${syt} pull_index '../repo' `realpath '../remote'` )

step 'rm file'
( cd 'repo' && ${syt} rm 'world.txt' )
if [[ -e 'repo/world.txt' ]]
then
    fail 'world.txt should no longer exist'
fi

step 'push removed file'
( cd 'repo' && ${syt} push '../remote' )
if [[ -e 'remote/world.txt' ]]
then
    fail 'world.txt should no longer exist'
fi
