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
    splits = block.split("\n")
    index = 0

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(splits) > 1 and splits[0].startswith("```") and splits[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        while index < len(splits):
            if splits[index][0] != ">":
                break
            if index == len(splits) - 1:
                return BlockType.QUOTE
            index += 1

    if block.startswith("- "):
        while index < len(splits):
            if splits[index][:2] != "- ":
                break
            if index == len(splits) - 1:
                return BlockType.ULIST
            index += 1

    if block.startswith("1. "):
        while index < len(splits):
            if splits[index][:3] != f"{index+1}. ":
                break
            if index == len(splits) - 1:
                return BlockType.OLIST
            index += 1

    return BlockType.PARAGRAPH
