import os
import shutil

def copy_files_recursive(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    contents = os.listdir(src)
    for item in contents:
        subpath_src = os.path.join(src, item)
        subpath_dst = os.path.join(dst, item)
        if os.path.isdir(subpath_src):
            copy_files_recursive(subpath_src, subpath_dst)
        elif os.path.isfile(subpath_src):
            shutil.copy(subpath_src, subpath_dst)


