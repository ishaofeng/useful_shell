#!/bin/bash
for i in `ls `
do
 mv $i "`echo $i|sed 's/org.springframework/sprfk/g'`";
done


