while :; do
    date
    curl -q http://royal-$1.socialgamenet.com/time.php
    echo
done
