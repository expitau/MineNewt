rm -rf ../save
# cp -r "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/Output" ../save
cp -r "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/V230500 Test" ../save
python3 main.py
rm -rf "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/Output"
cp -r ../save2 "/mnt/c/Users/Nathan/Data/Saved Games/Minecraft/Output"
