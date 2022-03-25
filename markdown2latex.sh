#! /bin/bash

for i in {1..14}
do
    if [ -e "logboek/week$i.md" ] && [ ! -e "logboek/tex/week$i.tex" ]
    then
        echo "converting week$i.md to week$i.tex"
        pandoc "logboek/week$i.md" -s -o "logboek/tex/week$i.tex"
    else
        if [ ! -e "logboek/week$i.md" ]
        then
            echo "file not found!"
        fi
        if [ -e "logboek/tex/week$i.tex" ]
        then
            echo "file already converted!"
        fi
    fi
done