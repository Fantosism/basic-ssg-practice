import os
from utils import copy_source_to_target

def main():
    script_dir = os.path.dirname(__file__)
    project_root = os.path.join(script_dir, "..")

    source = os.path.join(project_root, "static")
    target = os.path.join(project_root, "public")

    copy_source_to_target(source, target)

if __name__ == "__main__":
    main()
