import argparse, wget, requests, os, sys



parser = argparse.ArgumentParser("Scrape content from safebooru")

parser.add_argument("--tags",action="store",type=str,nargs="*",help="Tags to query by, defaults to all")
parser.add_argument("--output-folder",action="store",type=str,help="Folder to download images to")

# Set if you want to see an error message before the script quits (not actually implemented)
parser.add_argument("--show-1001-error",action="store",type=str,help="",metavar="",required=False,default=False, choices=["True","False"])


args = parser.parse_args()

include_tags = "%20".join(args.__getattribute__("tags"))
output_folder = args.__getattribute__("output_folder")
pages1001 = args.__getattribute__("show_1001_error")

try: os.mkdir(output_folder) 
except FileExistsError: print("Output folder exists")

print(include_tags,output_folder,pages1001)
#print(requests.get("https://safebooru.donmai.us/posts.json?page=1001").json()["message"])
# There is no reason to set this lower
# Since the maximum images to download is 200*1000 which is 200000 but you know
limit = 200

# Construct url
url = "https://safebooru.donmai.us/posts.json?tags={}&limit={}&page={}"


if pages1001 == "True":
    # Will go to page 1001
    secret = 1002
else: secret = 1001

# Show these fields, in specified order,
# Go check yourself all the options available

print(include_tags)
for i in range(1,secret):
    page = requests.get(url.format(include_tags,limit,i)).json()
    
    # This will also terminate when previously I had to manually catch IndexErrors
    if page == []:
        print("Page is empty... stopping")
        sys.exit()
        
    for item in page:
        print(i)
        # item is a dictionary
        
        if "file_url" in item:
            wget.download(item["file_url"],output_folder)
        