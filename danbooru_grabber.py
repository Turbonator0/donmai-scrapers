import wget, requests, sys, os

base_url = "https://danbooru.donmai.us/posts.json?tags={}%20rating:{}&limit={}&page={}"

ratings = ["e","q","s"]

limit = 200
include_tags = "%20".join(sys.argv[1:len(sys.argv)-1])
output_folder = sys.argv[len(sys.argv)-1]

while True:
    for rating in ratings:

        try:os.mkdir("{}/{}".format(output_folder,rating))
        except FileExistsError:print("Folder {} exists".format(rating))
        empty = False
        for page in range(1,1001):
            page_json = requests.get(base_url.format(include_tags,rating,limit,page)).json()
            for i in range(200):
                try:
                    if "file_url" in page_json[i]:
                        wget.download(page_json[i]["file_url"],"{}/{}".format(output_folder,rating))
                except IndexError:
                    if rating == ratings[2]:
                        print("no more files left for rating {}, quitting...".format(rating))
                        sys.exit()
                    else: 
                        print(base_url.format(include_tags,rating,limit,page))
                        print("no more files left for rating {}, moving along to next rating...".format(rating))
                        empty = True
                        break
            if empty == True:
                empty = False
                break