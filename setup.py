import hashlib

def parse(hash):
    folder_name = ""
    passed = False
    unparsed_folder_name = str(hash[0:2])[2:-1]
    return unparsed_folder_name

name = parse(hashlib.sha256("пидорас".encode()).digest())
with open(f"./{name}", "wb+") as f:
    f.write(hashlib.sha256("пидорас".encode()).digest())