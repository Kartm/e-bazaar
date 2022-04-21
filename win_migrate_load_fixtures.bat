@echo off

py -m manage migrate
for /f %%f in ('dir /B fixtures') do py -m manage loaddata fixtures\%%f
