方法一：
cat ~/plasma.log | sed 's/ /\n/g' | sed -r 's/-[[:digit:]].*-[[:digit:]]//g' | sed '/^$/d' > temp
cat temp | sudo pacman -Rs -

方法二：
grep -o '\b.*\-[[:digit:]].*\-[[:digit:]]\b' test > temp
cat temp | sudo pacman -Rs -

