#!/bin/bash
# 解决centos系统安装rpm包缺少依赖的问题
# 前提：yum可用
# 用法：rpm -ivh *.rpm 2>&1 | ./resolve-dep.sh

declare -A dic
echo "$(grep 'is needed by' $1 | sed 's/is needed by .*//')" | while read file; do
        package=$(yum whatprovides "${file}" | grep -E '.*-[0-9]+.*-[0-9]+\..*el[0-9].*\..*:.*' | head -n 1 | sed 's/^[0-9]\+://' | sed 's/-[0-9]\+.*-[0-9]\+\..*el[0-9].*\..*:.*$//')
        installed=${dic["${package}"]}
        if test -z "${installed}"; then
                yum install -y ${package}
                dic["${package}"]=1
        fi
done
