import wget, requests, sys, os

base_url = "https://danbooru.donmai.us/posts.json?tags={}%20rating:{}&limit={}&page={}"

ratings = ["e","q","s"]
user_ratings = []
MAXTAGS = 2
MAXTAGS_OFFSET = MAXTAGS + 1
TAG_COUNT = 3
TAG_OFFSET = TAG_COUNT + 1

limit = 200
include_tags = []

for args in range(len(sys.argv)):
    current_arg = sys.argv[args]
    if "--help" in sys.argv:
        print("""Current options are:
        -t\t\tfor tags
        -o\t\tfor output folder
        --help\t\tto display this message again""")
        sys.exit()
    if current_arg == "-o":
        try: output_folder = sys.argv[args+1]
        except IndexError: print("I cant fix this")
    elif current_arg == "-t":
        for i in sys.argv[args+1:args+MAXTAGS_OFFSET]:
            # stop at delimiter which is -
            if "-" in i:
                break
            else: include_tags.append(i)
    if current_arg == "-r":
        for rating in sys.argv[args+1:args+TAG_OFFSET]:
            if "-" in rating:
                break
            else: user_ratings.append(rating)

include_tags = "%20".join(include_tags)

for rating in ratings:
    try:os.mkdir("{}/{}".format(output_folder,rating))
    except FileExistsError:print("Folder {} exists".format(rating))

while True:
    for rating in user_ratings:
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
