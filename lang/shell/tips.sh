# cut more spaces as delimiter
bzcat debug.log.2012-06-1*.bz2 | grep photo_upload_stat_statck | sed 's/\s\s*/ /g' | cut -d' ' -f7

# replace files content on batch
sed -i "s/组件/应用/g" `grep "组件" -rl ./`

# 查看web server类型
curl -s --head "http://www.baidu.com"

# 查看cpu位数
getconf LONG_BIT

# 查看各种tcp连接状态的统计
netstat -ant|awk '{print $6}'|sort |uniq -c | sort -nr
