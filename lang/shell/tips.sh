# cut more spaces as delimiter
bzcat debug.log.2012-06-1*.bz2 | grep photo_upload_stat_statck | sed 's/\s\s*/ /g'|cut -d' ' -f 7

# replace files content on batch
sed -i "s/组件/应用/g" `grep "组件" -rl ./`

