# Metadata Details
# 5000NFTs
# Genesis Pass 4500
# Genesis Pass Ultra 500

import json
import random
import shutil
import pathlib 

# Configuration
COLLECTION_NAME = "Genesis Pass"
COLLECTION_SIZE = 5000
NORMAL_COUNT = 4500
ULTRA_COUNT = 500
OUTPUT_DIRECTORY_NAME = "assets"

with open("in/GP.json", "r") as data:
    # Reading from JSON file
    normal_metadata = json.load(data);

with open("in/GPU.json", "r") as data:
    # Reading from JSON file
    ultra_metadata = json.load(data);

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

        filename = "{name}.json".format(name = str(idx))
        path = "{dir}/{name}.json".format(dir = OUTPUT_DIRECTORY_NAME, name=str(idx))

        # write the metadata JSON
        with open(path, "w") as outfile:
            outfile.write(serialized_metadata)

        # write the PNG
        shutil.copy("in/GPU.png", "{outdir}/{index}.png".format(outdir=OUTPUT_DIRECTORY_NAME, index=idx))
    else:
        # apply metadata changes
        image_file = "{index}.png".format(index=idx)
        normal_metadata["name"] = COLLECTION_NAME + " #" + str(idx)
        normal_metadata["image"] = image_file
        normal_metadata["edition"] = idx
        normal_metadata["properties"]["files"][0]["uri"] = image_file

        serialized_metadata = json.dumps(normal_metadata, indent=4)

        filename = "{name}.json".format(name = str(idx))
        path = "{dir}/{name}.json".format(dir = OUTPUT_DIRECTORY_NAME, name=str(idx))

        # write the metadata JSON
        with open(path, "w") as outfile:
            outfile.write(serialized_metadata)

        # write the PNG
        shutil.copy("in/GP.png", "{outdir}/{index}.png".format(outdir=OUTPUT_DIRECTORY_NAME,index=idx))

# Create `collection.png` and `collection.json` files from first NFT
shutil.copy("assets/0.png", "assets/collection.png")
shutil.copy("assets/0.json", "assets/collection.json")

# Print Sanity Check Counts
normal_count = 0
ultra_count = 0

print("Distribution Map")
for i in range(COLLECTION_SIZE):
    path = "{dir}/{name}.json".format(dir = OUTPUT_DIRECTORY_NAME, name=str(i))
    with open(path, "r") as data:
        # metadata
        md = json.load(data);

    attr = md["attributes"][0]["value"]
    if attr == "Ultra":
        ultra_count += 1
        print("!", end="")
    elif attr == "Normal":
        normal_count += 1
        print("|", end="")

# ensure newline
print()

print("No. of Normal", normal_count, "/", NORMAL_COUNT, normal_count == NORMAL_COUNT)
print("No. of Ultra", ultra_count, "/", ULTRA_COUNT, ultra_count == ULTRA_COUNT)
