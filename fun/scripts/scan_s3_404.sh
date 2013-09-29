#!/bin/bash
#===========================
# a file contents
#===========================
#  21749 https://royal-us-asset.s3.amazonaws.com/v3/assets/pickups/pickupRing.swf<
#  13231 https://royal-us-asset.s3.amazonaws.com/v3/assets/pickups/pickupWatering_1000_10.swf<
#  11693 https://royal-us-asset.s3.amazonaws.com/v3/assets/pickups/pickupRoost.swf<
#   4963 https://royal-us-asset.s3.amazonaws.com/v3/assets/pickups/pickupBurningCandle.swf<
#===========================
cat a | awk '{print $2'} | cut -d'<' -f1 > b
for x in `cat b`; do
    echo $x
    curl -I $x 2>/dev/null | grep HTTP
    echo
done
