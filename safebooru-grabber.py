import wget, requests, sys

limit = 200
include_tags = '%20'.join(sys.argv[1:(len(sys.argv)-1)])
output_folder = sys.argv[len(sys.argv)-1]

url = "https://safebooru.donmai.us/posts.json?tags={}&limit={}&page={}"
while True:
    # we can only go up to page 1000
    for i in range(1,1001):
        page_json = requests.get(url.format(include_tags,limit,i)).json()
        for i in range(200):
            try: 
                if "file_url" in page_json[i]:
                    wget.download(page_json[i]["file_url"])
            except IndexError:
                print("Index, not found, quitting...")
                sys.exit()