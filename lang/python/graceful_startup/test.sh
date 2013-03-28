for i in `seq 10000`
do
    #telnet localhost 8990
    nc localhost 8990
    if [ $? -eq 0 ]; then
        echo 
    else
        echo $i
        exit
    fi
done
