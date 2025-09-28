from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split("\n\n")
    for item in splits:
        if item == "":
            continue
        item = item.strip()
        blocks.append(item)
    return blocks

def block_to_block_type(block):
    if "# " in block[:7]:
        return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    splits = block.split("\n")
    
    # Check quote
    index = 0
    while index < len(splits):
        if splits[index][0] != ">":
            break
        if index == len(splits) - 1:
            return BlockType.QUOTE
        index += 1

    # Check UList
    index = 0
    while index < len(splits):
        if splits[index][:2] != "- ":
            break
        if index == len(splits) - 1:
            return BlockType.ULIST
        index += 1

    # Check OList
    index = 0
    while index < len(splits):
        if splits[index][:3] != f"{index+1}. ":
            break
        if index == len(splits) - 1:
            return BlockType.OLIST
        index += 1

    return BlockType.PARAGRAPH
