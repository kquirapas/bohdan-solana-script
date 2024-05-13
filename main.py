# Metadata Details
# 5000NFTs
# Genesis Pass 4500
# Genesis Pass Ultra 500

import json
import random
import shutil
import pathlib 

 
def copy_and_rename(src_path, dest_path):
    # Copy the file
    shutil.copy(src_path, dest_path)

    # Rename the copied file
    # new_path = f"{dest_path}/{new_name}"
    # shutil.move(f"{dest_path}/{src_path}", new_path)

with open("in/GP.json", "r") as data:
    # Reading from JSON file
    normal_metadata = json.load(data);

with open("in/GPU.json", "r") as data:
    # Reading from JSON file
    ultra_metadata = json.load(data);


COLLECTION_NAME = "Genesis Pass"
COLLECTION_SIZE = 5000
NORMAL_COUNT = 4500
ULTRA_COUNT = 500

# list for indices of ultra passes
index_ultra_list = [];

for i in range(ULTRA_COUNT):
    # initialize random number
    # Solana starts at index 0
    n = random.randint(0, COLLECTION_SIZE - 1)
    while n not in index_ultra_list and len(index_ultra_list) != ULTRA_COUNT:
        index_ultra_list.append(n)
        n = random.randint(0, 4999)

is_ultra_list = [True if x in index_ultra_list else False for x in range(COLLECTION_SIZE)];


for idx, is_ultra in enumerate(is_ultra_list):
    if is_ultra: # ULTRA
        # apply metadata changes
        image_file = "{index}.png".format(index=idx)
        ultra_metadata["name"] = COLLECTION_NAME + " #" + str(idx)
        ultra_metadata["image"] = image_file
        ultra_metadata["edition"] = idx
        ultra_metadata["properties"]["files"][0]["uri"] = image_file

        serialized_metadata = json.dumps(ultra_metadata, indent=4)

        directory = "out"
        filename = "{name}.json".format(name = str(idx))
        path = "{dir}/{name}.json".format(dir = directory, name=str(idx))

        # write the metadata JSON
        with open(path, "w") as outfile:
            outfile.write(serialized_metadata)

        # write the PNG
        copy_and_rename("in/GPU.png", "out/{index}.png".format(index=idx))
    else:
        # apply metadata changes
        image_file = "{index}.png".format(index=idx)
        ultra_metadata["name"] = COLLECTION_NAME + " #" + str(idx)
        ultra_metadata["image"] = image_file
        ultra_metadata["edition"] = idx
        ultra_metadata["properties"]["files"][0]["uri"] = image_file

        serialized_metadata = json.dumps(normal_metadata, indent=4)

        directory = "out"
        filename = "{name}.json".format(name = str(idx))
        path = "{dir}/{name}.json".format(dir = directory, name=str(idx))

        # write the metadata JSON
        with open(path, "w") as outfile:
            outfile.write(serialized_metadata)

        # write the PNG
        copy_and_rename("in/GP.png", "out/{index}.png".format(index=idx))

# Print Sanity Check Counts
normal_count = 0
ultra_count = 0
for i in range(COLLECTION_SIZE):
    directory = "out"
    path = "{dir}/{name}.json".format(dir = directory, name=str(i))
    with open(path, "r") as data:
        # metadata
        md = json.load(data);

    attr = md["attributes"][0]["value"]
    if attr == "Ultra":
        ultra_count += 1
    elif attr == "Normal":

        normal_count += 1

print("No. of Normal", normal_count, "/", NORMAL_COUNT, normal_count == NORMAL_COUNT)
print("No. of Ultra", ultra_count, "/", ULTRA_COUNT, ultra_count == ULTRA_COUNT)
