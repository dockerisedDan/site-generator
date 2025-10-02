import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page

public_dir = "./public/"
static_dir = "./static/"
content_dir = "./content/"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_files_recursive(static_dir, public_dir)
    generate_page(os.path.join(content_dir, "index.md"), template_path, os.path.join(public_dir, "index.html"))

if __name__ == "__main__":
    main()

