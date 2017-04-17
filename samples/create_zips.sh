#!/bin/bash

# Zip each source directory
for i in */
do
    zip -r "${i%/}.zip" "$i"
done
