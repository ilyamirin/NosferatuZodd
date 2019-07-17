#! /bin/sh

clear

script_dir="${0%/*}"
python3 -m programy.clients.events.tcpsocket.client --config $script_dir/../../config/xnix/config.tcp.yaml --cformat yaml --logging $script_dir/../../config/xnix/logging.yaml

