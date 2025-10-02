import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    list_of_matches = []
    # pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" # boot.dev regex (read after completing myself)
    pattern = r"\!\[.*?\]\(.*?\)"
    matches = re.findall(pattern, text)
    for string in matches:
        string = string[2:len(string)-1]
        string = string.split("](")
        list_of_matches.append((string[0], string[1]))
    return list_of_matches


def extract_markdown_links(text):
    list_of_matches = []
    # pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" # boot.dev regex (read after completing myself)
    pattern = r"[\s\S]?\[.*?\]\(.*?\)"
    matches = re.findall(pattern, text)
    for string in matches:
        if string[0] == "!":
            continue
        if string[0] == "[":
            string = string[1:len(string)-1]
        else:
            string = string[2:len(string)-1]
        string = string.split("](")
        list_of_matches.append((string[0], string[1]))
    return list_of_matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        string = node.text
        images = extract_markdown_images(string)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            split = string.split(f"![{image[0]}]({image[1]})")
            if len(split) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.PLAIN))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            string = split[1] 
        if string != "":
            new_nodes.append(TextNode(string, TextType.PLAIN))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        string = node.text
        links = extract_markdown_links(string)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            split = string.split(f"[{link[0]}]({link[1]})")
            if len(split) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.PLAIN))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            string = split[1]
        if string != "":
            new_nodes.append(TextNode(string, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

