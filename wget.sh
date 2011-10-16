#!/bin/bash

for (( i = 0; i < 100 ; i ++ ))
do
    wget  --limit-rate=50k http://10.20.133.161:2301/selloffer/k-mp3_n-y.html
done
