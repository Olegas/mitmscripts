#!/bin/bash
./proxy_on.sh
mitmproxy --script ./local_proxy.py
./proxy_off.sh