#!/bin/bash

CTAGS=`which ctags-exuberant`;

OPTS="--language-force=python -L - "

find ./ -regextype posix-extended -iregex ".*py$" | ${CTAGS} ${OPTS}
