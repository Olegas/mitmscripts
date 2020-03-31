#!/bin/bash
source ./.adapter
networksetup -setwebproxystate ${ADAPTER} on
networksetup -setsecurewebproxystate ${ADAPTER} on