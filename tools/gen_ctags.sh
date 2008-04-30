#!/bin/bash

CTAGS=`which ctags-exuberant || which ctags`;

OPTS="--language-force=python -L - "

find ./ -regextype posix-extended -iregex ".*py$" | ${CTAGS} ${OPTS}
