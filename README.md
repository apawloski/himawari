# himawari

A basic tool for downloading the latest images from Himawari-8.

#### Background
Himawari-8 is a geostationary satellite operated by [JMA](https://en.wikipedia.org/wiki/Japan_Meteorological_Agency). It provides important data on Earth's weather and atmosphere, but I like it because it also posts pretty pictures of Earth every 10 minutes. This script grabs the latest image at a configurable resolution.

#### Installation
himawari can be installed by running (preferably from [virtualenv](https://virtualenv.readthedocs.org/en/latest/)):

    pip install -r requirements.txt

#### Configuring
Currently configuration is hardcoded in `himawari.py`. This will be externalized if I find the time to continue.

This project uses S3. It requires `~/.aws/config` and `~/.aws/credentials` files.

#### Running
You can run this script simply by:

    python himawari.py

It will save the latest image to `IMAGE_PATH` and post it to S3 based at `IMAGE_S3_BASE_BUCKET`

#### Credits
This script is based on glandium's [himawari-wallpaper](https://github.com/glandium/himawari-wallpaper).




