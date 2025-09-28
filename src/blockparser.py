def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split("\n\n")
    for item in splits:
        if item == "":
            continue
        item = item.strip()
        blocks.append(item)
    return blocks
