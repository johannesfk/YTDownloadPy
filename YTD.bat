@echo off
echo .
echo Updateting dependencies...
echo .

pip install -r requirements.txt

echo .
echo Updating done!
echo Running YTD Tool...
echo .

python YTDownload.py

pause