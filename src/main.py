import os
import shutil

def copy_files(src, dst):
    try:
        contents = os.listdir(src)
    except Exception as e:
        raise Exception(f"Unable to list files in {src}: {e}")
    for item in contents:
        subpath_src = os.path.join(src, item)
        subpath_dst = os.path.join(dst, item)
        if item.startswith("."):
            continue
        if os.path.isdir(subpath_src):
            try:
                os.makedirs(subpath_dst, exist_ok=True)
            except Exception as e:
                raise Exception(f"Unable to create directory {subpath_dst}: {e}")
            copy_files(subpath_src, subpath_dst)
        elif os.path.isfile(subpath_src):
            try:
                shutil.copy(subpath_src, subpath_dst)
            except Exception as e:
                raise Exception(f"Unable to copy file: {subpath_src} -> {subpath_dst}: {e}")

def main():
    public_dir = os.path.abspath("./public/")
    static_dir = os.path.abspath("./static/")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    try:
        os.makedirs(public_dir, exist_ok=True)
    except Exception as e:
        raise Exception(f"Unable to create directory {public_dir}: {e}")
    copy_files(static_dir, public_dir)

if __name__ == "__main__":
    main()

