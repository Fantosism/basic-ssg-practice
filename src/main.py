import os
import sys
from utils import copy_source_to_target, generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    script_dir = os.path.dirname(__file__)
    project_root = os.path.join(script_dir, "..")

    static_path = os.path.join(project_root, "static")
    docs_path = os.path.join(project_root, "docs")
    content_path = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    copy_source_to_target(static_path, docs_path)
    generate_pages_recursive(content_path, template_path, docs_path, basepath)

if __name__ == "__main__":
    main()
