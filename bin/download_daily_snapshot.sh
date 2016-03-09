#! /bin/bash

# Downloads 24 hours of images from 15:00 yesterday to 15:00 today

today=$(date +'%Y%m%d')
yesterday=$(date --date="yesterday" +'%Y%m%d')

# Grab the portion from yesterday
for t in `seq 150000 1000 235000` ; do
    aws s3 cp "s3://earth.apawl.com/earth_imagesequence/Himawari$yesterday$t.png" . --region us-east-1
done

# Grab the portion from today
for t in `seq 00000 1000 150000`; do
    d=$(printf "%06d\n" $t)
    aws s3 cp 's3://earth.apawl.com/earth_imagesequence/Himawari$today$d.png' . --region us-east-1
done






