import argparse, wget, requests, os, sys, re, urllib

# boilerplate
parser = argparse.ArgumentParser()

parser.add_argument("--output-folder",action="store",type=str,help="Folder to download images to")

# Optional
# This will download the newest images without consideration for tags if left empty
parser.add_argument("--tags",action="store",type=str,nargs="*",required=False,help="Tags to query by, defaults to all",default="")
parser.add_argument("--ratings", action="store",type=str,nargs="*",required=False,help="Ratings to download by (order MATTERS)",default=["e","q","s"])

args = parser.parse_args().__dict__
# args.__getattribute__ lol

include_tags = "%20".join(args["tags"])
output_folder = args["output_folder"]
search_ratings = args["ratings"]

url = "https://danbooru.donmai.us/posts.json?tags={}%20rating:{}&limit={}&page={}"
limit = 200

# create parent directory
try:os.mkdir(output_folder)
except FileExistsError: print("Parent directory exists")

# create subdirectories
for rating in search_ratings:
    try:os.mkdir(f"{output_folder}/{rating}")
    except FileExistsError: print(f"Folder: {output_folder}/{rating} exists")


# By rating
for rating in search_ratings:
    # By page
    for page_n in range(1,1001):
        # By entry of page

        page = requests.get(url.format(include_tags,rating,limit,page_n)).json()
        if page == []:
            break # break for loop
        for item in page:
            
            if "file_url" in item:

                file_location = output_folder+"/"+rating
                try: wget.download(item["file_url"],file_location)

                # This gets raised for some reason, I do not know why
                except urllib.error.URLError: break