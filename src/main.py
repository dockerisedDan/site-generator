import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_content_recursive

public_dir = "./public/"
static_dir = "./static/"
content_dir = "./content/"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files...")
    copy_files_recursive(static_dir, public_dir)
    print("Generating content...")
    generate_content_recursive(content_dir,template_path, public_dir)

if __name__ == "__main__":
    main()

