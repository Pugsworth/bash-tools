#!/usr/bin/env sh

function default() {
    local arg2=$2;
    local arg1=${1:-$2};

    echo $arg1;
}

function git_whois() {
    local who=$(git -C "$1" config --get remote.origin.url | sed -n "s/.*\.com\/\([^\/]\+\).*/\1/p")
    echo $(default "$who" " LOCAL");
}

find $1 -name ".git" -print0 | while read -d '' f;
do
    gdir=${f%%.git};
    printf "%-15s -> %s\n" $(git_whois "$gdir") "$gdir";
done
