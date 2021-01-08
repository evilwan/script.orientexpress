#!/bin/sh
#
# Create zip installer for add-on
#

VERSION=`cat VERSION`
OUTFILE=script.orientexpress-${VERSION}.zip

pushd .
cd ..
zip -r ${OUTFILE} script.orientexpress/*
popd
