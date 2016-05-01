#! /bin/bash

app_name="CoDA"
#app_name="animate"
rm -rvf dist/$app_name.app/Contents/Resources/sprites
cp -rvf animate.py balancing.py characters.py coda.py sprites ./dist/$app_name.app/Contents/Resources/
cp -rvf Info.plist ./dist/$app_name.app/Contents/
