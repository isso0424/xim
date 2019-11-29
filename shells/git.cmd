@echo off
setlocal
git config --unset http.proxy
git config --unset https.proxy
git config --global http.proxy %1
git config --global https.proxy %2
