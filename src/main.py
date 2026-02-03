import os
from utils import copy_source_to_target, generate_pages_recursive


def main():
    script_dir = os.path.dirname(__file__)
    project_root = os.path.join(script_dir, "..")

    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")
    content_path = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    copy_source_to_target(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)

if __name__ == "__main__":
    main()
