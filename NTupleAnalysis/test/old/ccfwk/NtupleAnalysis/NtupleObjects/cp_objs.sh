#!/bin/bash

if [ $# -ne 2 ]; then
  echo "\n @@@ FATAL -- only 2 arguments allowed (input path and CMSSW package name). stopping execution.\n"
  return
fi

IPATH=$1
SWPKG=$2

if [ -d inc/ ]; then
  mv inc inc_old
fi

if [ -d src/ ]; then
  mv src src_old
fi

cp -r "$IPATH"/interface inc
cp -r "$IPATH"/src src

if [ -f src/classes_def.xml ]; then
  rm src/classes_def.xml
fi

if [ -f src/classes.h ]; then
  rm src/classes.h
fi

sed -i "s|$SWPKG/interface/|inc/|g" src/*
sed -i "s|$SWPKG/interface/|inc/|g" inc/*

unset -v IPATH SWPKG
