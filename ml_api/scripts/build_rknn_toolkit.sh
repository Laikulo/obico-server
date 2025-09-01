#!/usr/bin/env bash

set -ex
set -o pipefail

DOCKER=${DOCKER:-docker}

VERSION=
PREFIX=thespaghettidetective
INSECURE=

while getopts v:p:i flag
do
    case "$flag" in
        v) VERSION=${OPTARG};;
        p) PREFIX=${OPTARG};;
        i) INSECURE="--insecure";;
        *)
        	echo >&2 "Unexpected flag $flag"
        	exit 2
        	;;
    esac
done

typeset -a PLATFORMS
PLATFORMS=(amd64 arm64)

CONTAINER_SPEC="${PREFIX}/rknn_toolkit:${VERSION}"

manifest_hash="$($DOCKER manifest create ${INSECURE} "${CONTAINER_SPEC}" | tee /dev/stderr)"
for platform in "${PLATFORMS[@]}"; do
  $DOCKER build --platform linux/"$platform" -f Dockerfile.rknn_toolkit_"$platform" --manifest "$manifest_hash"
done

$DOCKER manifest push ${INSECURE} "${CONTAINER_SPEC}"