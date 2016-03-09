#! /bin/bash

# This is a completely ad-hoc approach. Just for fun.

# Get the latest image
python himawari.py

# Use expose to create the latest site
cd site
rm -rf _site
aws s3 cp s3://earth.apawl.com/site . --recursive --region 'us-east-1'
/usr/bin/Expose/expose.sh
aws s3 cp _site/ s3://earth.apawl.com/ --recursive --region 'us-east-1'
aws s3 cp _site/ s3://earth.apawl.com/now/ --recursive --region 'us-east-1'
cd - 
