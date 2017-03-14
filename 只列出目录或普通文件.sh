ls -Al | grep '^-' | awk '{print $9}'
ls -Al | grep '^d' | awk '{print $9}'
