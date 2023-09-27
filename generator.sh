#/bin/bash!
#! C:\Windows\System32\bash.exe
pcname="ronit"
venv="pyCodelabs"
projectlocation="Desktop/Python/CAT1_CompGraphics"
pythonFile="main.py"

cd /c/Users/$pcname/$venv
#sleep 3
source ./Scripts/Activate
cd /c/Users/$pcname/$projectlocation
python $pythonFile
# Deactivate the virtualenv
deactivate

#python /path/to/python/script.py