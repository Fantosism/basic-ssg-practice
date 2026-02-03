import os
from utils import copy_source_to_target, generate_page


def main():
    script_dir = os.path.dirname(__file__)
    project_root = os.path.join(script_dir, "..")

    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")
    content_path = os.path.join(project_root, "content", "index.md")
    template_path = os.path.join(project_root, "template.html")
    dest_path = os.path.join(project_root, "public", "index.html")

    copy_source_to_target(static_path, public_path)
    generate_page(content_path, template_path, dest_path)

if __name__ == "__main__":
    main()
