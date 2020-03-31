#!/bin/bash
source ./.adapter
networksetup -setwebproxy ${ADAPTER} 127.0.0.1 8080
networksetup -setsecurewebproxy ${ADAPTER} 127.0.0.1 8080