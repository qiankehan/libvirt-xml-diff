#!/bin/bash -x
#===============================================================================
#
#          FILE: gen-example.sh
# 
#         USAGE: ./gen-example.sh 
# 
#   DESCRIPTION: Generate test files for the project
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 05/19/2016 10:18
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
GIT_DIR=./libvirt
OUT_DIR=../examples/patch
cd $GIT_DIR
mkdir -p $OUT_DIR
git pull
#$TEST_BRANCH=master
#$CURRENT_COMMIT=$(git log -n 1  --pretty=format:%H)
#git branch|grep -q $TEST_BRANCH
#if [ $? -ne 0 ];then
#    git checkout -b $TEST_BRANCH
#fi
i=0
for commmit in $(git log --pretty="format:%H" --follow docs/schemas/);do
    dir_name=$commmit-$(git show --quiet --pretty="format:%ct" $commmit)
    git checkout $commmit
    mkdir -p $OUT_DIR/$dir_name
    changed_files=$(git show --pretty="format:" --name-only $commmit|grep rng)
    for file in $changed_files;do
        #cp $file $OUT_DIR/$dir_name/$(basename $file).new
        cp docs/schemas/* $OUT_DIR/$dir_name/
    done

    git checkout HEAD~1
    for file in $changed_files;do
        cp $file $OUT_DIR/$dir_name/$(basename $file).old
    done
    
    if [ $i -eq 30 ] ; then
        break
    fi
    i=`expr $i + 1`
done
git reset
git checkout master
sed -i 's|xmlns="http://relaxng.org/ns/structure/1.0"||g' $(find $OUT_DIR -name '*rng*'|tr '\n' ' ')
