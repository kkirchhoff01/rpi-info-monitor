#!/bin/bash

OLD_PATH=$(pwd)
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
clear && python3 -m display $@
cd $OLD_PATH
