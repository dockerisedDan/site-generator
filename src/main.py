import os
import sys
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_content_recursive

public_dir = "./docs/"
static_dir = "./static/"
content_dir = "./content/"
template_path = "./template.html"

def main():
    basepath = "/"
    args = sys.argv
    if len(args) > 2:
        print("Usage: main [basepath]")
        print("basepath defaults to /")
        return -1
    elif len(args) == 2:
        basepath = args[1]
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files...")
    copy_files_recursive(static_dir, public_dir)
    print("Generating content...")
    generate_content_recursive(content_dir,template_path, public_dir, basepath)

main()

