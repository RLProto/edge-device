#!/bin/bash
set -ex

echo "[INFO] Updating script files.."
cd ~/sodavision
git stash
git pull --rebase 
git stash pop
