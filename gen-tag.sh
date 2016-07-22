#!/bin/bash - 
#===============================================================================
#
#          FILE: gen-tag.sh
# 
#         USAGE: ./gen-tag.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 07/21/2016 16:34
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
OWD=$(pwd)
cd $1
for ver in $(git tag|grep 'v[1-9]\.[0-9]\+\.[0-9]\+$');do
    if [ -f $OWD/examples/$ver ];then
        continue
    fi
    git checkout $ver
    cp -r ./docs/schemas $OWD/examples/$ver
done
git checkout master
sed -i 's|xmlns="http://relaxng.org/ns/structure/1.0"||g' $(find $OWD/examples/v* -name '*rng*'|tr '\n' ' ')
