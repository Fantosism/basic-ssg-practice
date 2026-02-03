import os
import shutil

from markdown import markdown_to_html_node, extract_title


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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page: {os.path.relpath(from_path)} -> {os.path.relpath(dest_path)} using {os.path.relpath(template_path)}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Content }}", html_content).replace("{{ Title }}", title)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Scanning directory: {os.path.relpath(dir_path_content)}")
    items = os.listdir(dir_path_content)
    for item in items:
        source_path = os.path.join(dir_path_content, item)
        is_file = os.path.isfile(source_path)
        if is_file:
            if item.endswith(".md"):
                dest_file = item.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_file)
                print(f"  Generating: {os.path.relpath(source_path)} -> {os.path.relpath(dest_path)}")
                generate_page(source_path, template_path, dest_path)
            else:
                print(f"  Skipping non-markdown file: {item}")
        else:
            new_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(source_path, template_path, new_dest_path)
