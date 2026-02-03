import os
import shutil

def copy_source_to_target(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)

    os.mkdir(target)

    items = os.listdir(source)
    for item in items:
        is_file = os.path.isfile(os.path.join(source, item))
        if is_file:
            shutil.copy(os.path.join(source, item), target)
        else:
            copy_source_to_target(os.path.join(source, item), os.path.join(target, item))