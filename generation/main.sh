rm -rf saves/save
# cp -r "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/Output" ../save
cp -r "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/V230500 Test" saves/save
python3 src/main.py
rm -rf "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/Output"
cp -r saves/save2 "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/Output"
