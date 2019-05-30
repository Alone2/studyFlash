python3 -m PyInstaller -F study.py --distpath ./compiled --workpath ./build &&
cp settings.json compiled/settings.json &&
echo DONE 
