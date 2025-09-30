from enum import Enum
from htmlnode import  ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from textparser import text_to_textnodes


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

def heading_to_html_node(block):
    count = 0
    for index in range(len(block)):
        if block[index] != "#" or index == 6:
            break
        count += 1
    text = block.lstrip("# ")
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return ParentNode(tag=f"h{count}", children=children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = ""
    for line in lines:
        text += line + " "
    text = text.strip()
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return ParentNode(tag="p", children=children)

def code_to_html_node(block):
    lines = block.split("\n")
    text = []
    for line in lines:
        if line == "```":
            continue
        text.append(line) 
    text = "\n".join(text).rstrip()
    text_node = TextNode(text, TextType.PLAIN)
    code_child = text_node_to_html_node(text_node)
    code_node = ParentNode(tag="code", children=[code_child])
    return ParentNode(tag="pre", children=[code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    text = ""
    for line in lines:
        text += line.strip(">").strip() + " "
    text = text.strip()
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return ParentNode(tag="blockquote", children=children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line.strip("-").strip()
        text_nodes = text_to_textnodes(text)
        children = []
        for text_node in text_nodes:
            children.append(text_node_to_html_node(text_node))
        list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=list_items)

def olist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for index in range(len(lines)):
        text = lines[index].lstrip(f"{index+1}.").strip()
        text_nodes = text_to_textnodes(text)
        children = []
        for text_node in text_nodes:
            children.append(text_node_to_html_node(text_node))
        list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=list_items)

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_node = block_to_html_node(block)
        nodes.append(block_node)
    parent = ParentNode(tag="div", children=nodes)
    return parent

