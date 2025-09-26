import unittest
from textnode import TextNode, TextType
from textparser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter


class TestTextParser(unittest.TestCase):
    # Inline text types tests

    def test_delim_bold(self):
        node =  TextNode("This is text with a **bolded** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.PLAIN),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_italic(self):
        node = TextNode("This is text with an __italic__ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_bold_and_italic(self):
        node = TextNode("**Bold** and __italic__", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", TextType.ITALIC)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected)

    # Image extraction tests

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_starts_with_image(self):
        matches = extract_markdown_images("![This image](https://i.imgur.com/zjjcJKZ.png) is at the start of the string")
        self.assertEqual([("This image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(expected, matches)

    def test_extract_markdown_image_with_link(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertEqual(expected, matches)

    # Link extraction tests

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.boot.dev)")
        self.assertEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_starts_with_link(self):
        matches = extract_markdown_links("[This link](https://www.boot.dev) is at the start of the string")
        self.assertEqual([("This link", "https://www.boot.dev")], matches)


    def test_extract_markdown_multi_links(self):
        matches = extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(expected, matches)

    def test_extract_markdown_link_with_image(self):
        matches = extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertEqual(expected, matches)


