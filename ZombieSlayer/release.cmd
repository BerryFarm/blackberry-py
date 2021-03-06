@echo off
rem Note: this app is useless without -devMode so we can't release it signed.
echo Remember to turn off ACCESS_SHARED!
if not exist _buildId echo 0>_buildId
call blackberry-nativepackager -package ZombieSlayer.bar ^
    -configuration Device-Release ^
    -devMode ^
    -target bar ^
    -env PYTHONPATH=app/native ^
    -env PYTHONDONTWRITEBYTECODE=1 ^
    -arg -qml -arg app/native/assets/main.qml ^
    -arg app/native/blackberry_tart.py ^
    bar-descriptor.xml ^
    icon.png ^
    *.py ^
    assets/ ^
    -C ../tart/entry ../tart/entry/TartStart.so ^
    -C ../tart/python ../tart/python/* ^
    -C ../tart/js ../tart/js/*.js ^
    -debugToken ../debugtoken.bar
