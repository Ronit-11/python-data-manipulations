#/bin/bash!
#! C:\Windows\System32\bash.exe
pcname="ronit"
venv="pyCodelabs"
projectlocation="Desktop/Python/CAT1_CompGraphics"
pythonFile="main.py"
#functiontocall="en_XX_fileGenerator"

cd /c/Users/$pcname/$venv

source ./Scripts/Activate
cd /c/Users/$pcname/$projectlocation
python $pythonFile

#to run a function of a file:
#python -c "from $pythonFile import $functiontocall; $functiontocall()"

# Deactivate the virtualenv
deactivate
