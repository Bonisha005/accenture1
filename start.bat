@echo off

echo Starting Flask backend...
cd retail_agents
call venv\Scripts\activate
start cmd /k python api_main.py

timeout /t 3

echo Starting React frontend...
cd ..\retail-dashboard
call npm install
start cmd /k npm run dev

timeout /t 2

start http://localhost:5173