for i in `seq 10000`
do
    sleep 2
    ./server.py 
    if [ $? -eq 0 ]; then
        echo 
    else
        echo $i
        exit
    fi
done
