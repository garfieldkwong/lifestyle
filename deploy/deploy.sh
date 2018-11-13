#!/bin/bash
DIR="$( dirname "${BASH_SOURCE[0]}" )"
cp -f ${DIR}/bin/* /usr/bin/
cp -f ${DIR}/service/* /etc/systemd/system/
