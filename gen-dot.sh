#!/bin/bash - 
#===============================================================================
#
#          FILE: gen-dot.sh
# 
#         USAGE: ./gen-dot.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 05/13/2016 17:13
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

for rng in ~/Software/libvirt/docs/schemas/*rng; do
    src=$(echo $rng|grep -o '[a-z]\+\.rng'|grep '\.rng'|sed 's/....$//')
    for dst in $(grep href $rng|grep -o '[a-z]\+\.rng'|grep '\.rng'|sed 's/....$//');do
        content="$src -> $dst;"
        sed -i "3 i \ $content" ./graph.dot
    done
done

