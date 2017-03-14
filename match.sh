#!/usr/bin/env bash

################################################################################
#     写代码时是不是经常遇到要用一个变量时，却忘记了这个变量是在哪个文件定义的 #
# 了？虽然有find这样的工具，但是find只能查找文件名；还有grep，但是grep可以查找 #
# 单个文件，查找多个文件却不方便。                                             #
#     这个脚本就是用来查找一个目录下包含某个关键字的所有文件，把关键字出现的那 #
# 一行内容和行号显示出来。                                                     #
# 用法：./match.sh [[-A|-B|-C] <NUM>] regexp dir                               #
#       当然，也可以把此脚本加入到PATH变量中                                   #
# 解释：-A NUM, --after-context=NUM         将匹配到的后NUM行也显示出来        #
#       -B NUM, --before-context=NUM        将匹配到的前NUM行也显示出来        #
#       -C NUM, --context=NUM               将匹配到的前NUM行和后NUM行都显示出 #
#                                           来，默认此选项                     #
#       NUM默认为1                                                             #
#                                                       Yotta Liu, 2016        #
################################################################################

if [ $# == 2 ]
then
    option="-C"
    num="1"
    regexp=${1}
    dir=${2}
elif [ $# == 3 ]
then
    option="-C"
    num=${1}
    regexp=${2}
    dir=${3}
else [ $# == 4 ]
    option=${1}
    num=${2}
    regexp=${3}
    dir=${4}
fi

for file in `find ${dir} -type f`
do
    file ${file} | grep 'text' > /dev/null
    if [ $? == 0 ]
    then
        grep ${regexp} ${file} > /dev/null
        if [ $? == 0 ]
        then
            echo -e "\n\033[34m==> ${file}\033[0m"
            grep -n --color=auto ${option} ${num} ${regexp} ${file}
		fi
	fi
done
