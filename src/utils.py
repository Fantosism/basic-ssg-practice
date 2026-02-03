import os
import shutil

def copy_source_to_target(source, target):
    if os.path.exists(target):
        print(f"Removing existing directory: {os.path.relpath(target)}/")
        shutil.rmtree(target)

    print(f"Creating fresh directory: {os.path.relpath(target)}/")
    os.mkdir(target)

    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        target_path = os.path.join(target, item)
        is_file = os.path.isfile(os.path.join(source, item))
        if is_file:
            print(f"Copying file: {os.path.relpath(source_path)} -> {os.path.relpath(target_path)}")
            shutil.copy(source_path, target)
        else:
            print(f"Entering directory: {item}")
            copy_source_to_target(source_path, target_path)