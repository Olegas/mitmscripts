#!/bin/bash
source ./.adapter
networksetup -setwebproxystate ${ADAPTER} off
networksetup -setsecurewebproxystate ${ADAPTER} off