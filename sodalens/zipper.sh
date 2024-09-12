#!/bin/bash

NAME=$(zenity --entry --title="Coloque o projeto que voce quer zipar")
if [ -n "$NAME" ]
then
    cd $HOME/Desktop/datasets
    zip -r $HOME/Desktop/datasets/$NAME.zip $NAME
fi