@echo off
setlocal
if not %1 == "" (
    npm config set proxy %1
) else (
    npm config delete proxy
)

if not %2 == "" (
    npm config set https-proxy %2
) else (
    npm config delete https-proxy
)
