import os
from blockparser import BlockType, markdown_to_html_node, markdown_to_blocks, block_to_block_type, heading_to_html_node

def generate_page(src_path, template_path, dst_path):
    print(f"Generating page from {src_path} -> {dst_path} using {template_path}")
    f = open(src_path, "r")
    src_file = f.read()
    f.close()
    f = open(template_path, "r")
    template_file = f.read()
    f.close()
    md_conv_html = markdown_to_html_node(src_file).to_html()
    page_title = extract_heading(src_file)
    gen_file = template_file.replace("{{ Title }}", page_title)
    gen_file = gen_file.replace("{{ Content }}", md_conv_html)
    dest_dir = os.path.dirname(dst_path)
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except Exception as e:
        raise Exception(f"Unable to create directory {dest_dir}: {e}")
    with open(dst_path, "w") as f:
        f.write(gen_file)
        f.close()

def extract_heading(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type != BlockType.HEADING:
            continue
        heading_node = heading_to_html_node(block)
        if heading_node.tag != "h1":
            continue
        if heading_node.children is not None:
            heading = ""
            for child in heading_node.children:
                heading += child.value
            return heading
    raise Exception("no h1 heading blocks found in markdown")


