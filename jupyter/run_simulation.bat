@echo off
start /b python integration_router.py
timeout /t 10
start /b python integration_node.py
timeout /t 5100
taskkill /im python.exe /f