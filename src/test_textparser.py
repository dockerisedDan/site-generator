import unittest
from test_textnode import TestTextNode
from textnode import TextNode, TextType
from textparser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_images, split_nodes_links


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

    # Split nodes images tests

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_with_link(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a [link](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_start(self):
        node = TextNode("![This image](https://www.boot.dev) is at the start of the string", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("This image", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" is at the start of the string", TextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_with_no_images(self):
        node = TextNode("This string has no links", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        self.assertListEqual([node], new_nodes)

    def test_split_with_link(self):
        node = TextNode("This string has a [link](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        self.assertListEqual([node], new_nodes)

    def test_only_image(self):
        node = TextNode("![Image](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("Image", TextType.IMAGE, "https://www.boot.dev"),
        ]
        self.assertListEqual(expected, new_nodes)

    # Split nodes links tests

    def test_split_links(self):
        node = TextNode("This is a text node with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        expected = [
            TextNode("This is a text node with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_with_images(self):
        node = TextNode("This is a text node with a link [to boot dev](https://www.boot.dev) and an ![image](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        expected = [
            TextNode("This is a text node with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and an ![image](https://www.youtube.com/@bootdotdev)", TextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[This link](https://www.boot.dev) is at the start of the string", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        expected = [
            TextNode("This link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is at the start of the string", TextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_with_no_link(self):
        node = TextNode("This string has no links", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    def test_split_with_image(self):
        node = TextNode("This string has an ![image](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    def test_only_link(self):
        node = TextNode("[Link](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        expected = [
            TextNode("Link", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertListEqual(expected, new_nodes)
