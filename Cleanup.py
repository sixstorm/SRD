import os, os.path

# Get all files and then remove
for file in os.listdir('temp'):
    print("Removing %s" % file)
    os.remove("temp/"+file)