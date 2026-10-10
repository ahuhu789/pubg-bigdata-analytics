@echo off
title Cassandra Worker Node 2 - PUBG Big Data
color 0A
echo ========================================================
echo  KHOI DONG APACHE CASSANDRA WORKER NODE (MAY 2)
echo  IP May 2: 192.168.1.23  --^>  Ket noi Seed May 1: 192.168.1.175
echo ========================================================
cd /d "%~dp0\.."
python scripts\run_node2.py
pause
