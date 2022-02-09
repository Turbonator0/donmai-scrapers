import wget, requests, sys

# assumes you are not using a gold/plat account, I have not added auth keys yet
MAXTAGS = 2
MAXTAGS_OFFSET = MAXTAGS + 1
limit = 200
include_tags = []
# This does something
for args in range(len(sys.argv)):
    current_arg = sys.argv[args]
    if "--help" in sys.argv:
        print("""Current options are:
        -t\t\tfor tags
        -o\t\tfor output folder
        --help\t\tto display this message again""")
        sys.exit()
    if current_arg == "-o":
        output_folder = sys.argv[args+1]
    elif current_arg == "-t":
        for i in sys.argv[args+1:args+MAXTAGS_OFFSET]:
            # stop at delimiter which is -
            if "-" in i:
                break
            else: include_tags.append(i)
    
include_tags = "%20".join(include_tags)

url = "https://safebooru.donmai.us/posts.json?tags={}&limit={}&page={}"
while True:
    # we can only go up to page 1000
    for i in range(1,1001):
        page_json = requests.get(url.format(include_tags,limit,i)).json()
        for i in range(200):
            try: 
                if "file_url" in page_json[i]:
                    wget.download(page_json[i]["file_url"],output_folder)
            except IndexError:
                print("Index, not found, quitting...")
                sys.exit()