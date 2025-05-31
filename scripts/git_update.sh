#!/bin/bash

VERSION=""

# get parameters
while getopts v: flag
do
  case "${flag}" in
    v) VERSION=${OPTARG};;
  esac
done

CURRENT_VERSION=`grep -E 'version' pyproject.toml | cut -d'=' -f2 | tr -d '"'`

if [[ $CURRENT_VERSION == '' ]]
then
  CURRENT_VERSION='v0.0.1'
fi

# replace . with space so can split into an array
CURRENT_VERSION_PARTS=(${CURRENT_VERSION//./ })

# get number parts
VNUM1=${CURRENT_VERSION_PARTS[0]}
VNUM2=${CURRENT_VERSION_PARTS[1]}
VNUM3=${CURRENT_VERSION_PARTS[2]}

if [[ $VERSION == 'major' ]]
then
  VNUM1=$((VNUM1+1))
  VNUM2=0
  VNUM3=0
elif [[ $VERSION == 'minor' ]]
then
  VNUM2=$((VNUM2+1))
  VNUM3=0
elif [[ $VERSION == 'patch' ]]
then
  VNUM3=$((VNUM3+1))
else
  echo "No version type (https://semver.org/) or incorrect type specified, try: -v [major, minor, patch]"
  exit 1
fi

# create new tag
NEW_TAG="$VNUM1.$VNUM2.$VNUM3"

cat ./pyproject.toml | sed -e "s/version.*/version = \"${NEW_TAG}\"/g" > ./pyproject.toml.new
mv ./pyproject.toml.new ./pyproject.toml

echo $NEW_TAG
