import unittest

from blockparser import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestBlockParser(unittest.TestCase):
    # Block splitting tests

    def test_block_splitting(self):
        markdown = "# This is a heading\n\n"
        markdown += "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        markdown += "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    def test_whitespace(self):
        markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n        - This is a list item\n        - This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    def test_extra_lines(self):
        markdown = "# This is a heading\n\n"
        markdown += "\n\n"
        markdown += "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        markdown += "\n\n"
        markdown += "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    def test_uneven_newlines(self):
        markdown = "# This is a heading\n\n"
        markdown += "\n\n\n"
        markdown += "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        markdown += "\n\n\n\n\n\n\n\n\n\n"
        markdown += "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    # Block type tests

    def test_headings(self):
        heading1 = "# This is heading 1"
        heading2 = "## This is heading 2"
        heading3 = "### This is heading 3"
        heading4 = "#### This is heading 4"
        heading5 = "##### This is heading 5"
        heading6 = "###### This is heading 6"
        block_type1 = block_to_block_type(heading1)
        block_type2 = block_to_block_type(heading2)
        block_type3 = block_to_block_type(heading3)
        block_type4 = block_to_block_type(heading4)
        block_type5 = block_to_block_type(heading5)
        block_type6 = block_to_block_type(heading6)
        self.assertEqual(BlockType.HEADING, block_type1)
        self.assertEqual(BlockType.HEADING, block_type2)
        self.assertEqual(BlockType.HEADING, block_type3)
        self.assertEqual(BlockType.HEADING, block_type4)
        self.assertEqual(BlockType.HEADING, block_type5)
        self.assertEqual(BlockType.HEADING, block_type6)

    def test_invalid_headings(self):
        bad_heading1 = "#This heading should fail"
        bad_heading2 = "####### This heading has too many #"
        block_type1 = block_to_block_type(bad_heading1)
        block_type2 = block_to_block_type(bad_heading2)
        self.assertNotEqual(BlockType.HEADING, block_type1)
        self.assertNotEqual(BlockType.HEADING, block_type2)

    def test_code_blocks(self):
        codeblock1 = "```This is a code block in one line\n```"
        codeblock2 = "```This is a code block\nthat uses 2 lines\n```"
        block_type1 = block_to_block_type(codeblock1)
        block_type2 = block_to_block_type(codeblock2)
        self.assertEqual(BlockType.CODE, block_type1)
        self.assertEqual(BlockType.CODE, block_type2)

    def test_bad_code_blocks(self):
        bad_codeblock1 = "```This code block is not closed"
        bad_codeblock2 = "This code block is not opened"
        bad_codeblock3 = "`This code block uses single ticks`"
        bad_codeblock4 = "```This code block doesn't use a newline```"
        block_type1 = block_to_block_type(bad_codeblock1)
        block_type2 = block_to_block_type(bad_codeblock2)
        block_type3 = block_to_block_type(bad_codeblock3)
        block_type4 = block_to_block_type(bad_codeblock4)
        self.assertNotEqual(BlockType.CODE, block_type1)
        self.assertNotEqual(BlockType.CODE, block_type2)
        self.assertNotEqual(BlockType.CODE, block_type3)
        self.assertNotEqual(BlockType.CODE, block_type4)

    def test_quotes(self):
        quote1 = ">This is a quote"
        quote2 = "> This is also a quote"
        quote3 = ">This is a quote\n>On multiple lines"
        quote4 = "> This quote also\n> Uses multiple lines"
        block_type1 = block_to_block_type(quote1)
        block_type2 = block_to_block_type(quote2)
        block_type3 = block_to_block_type(quote3)
        block_type4 = block_to_block_type(quote4)
        self.assertEqual(BlockType.QUOTE, block_type1)
        self.assertEqual(BlockType.QUOTE, block_type2)
        self.assertEqual(BlockType.QUOTE, block_type3)
        self.assertEqual(BlockType.QUOTE, block_type4)

    def test_bad_quotes(self):
        bad_quote1 = "This is not a quote"
        bad_quote2 = ">This is a quote\nWithout a >"
        bad_quote3 = "This quote is also\n>Missing the >"
        block_type1 = block_to_block_type(bad_quote1)
        block_type2 = block_to_block_type(bad_quote2)
        block_type3 = block_to_block_type(bad_quote3)
        self.assertNotEqual(BlockType.QUOTE, block_type1)
        self.assertNotEqual(BlockType.QUOTE, block_type2)
        self.assertNotEqual(BlockType.QUOTE, block_type3)

    def test_u_list(self):
        ulist1 = "- This is a ulist"
        ulist2 = "- This is a ulist\n- With 2 lines"
        block_type1 = block_to_block_type(ulist1)
        block_type2 = block_to_block_type(ulist2)
        self.assertEqual(BlockType.ULIST, block_type1)
        self.assertEqual(BlockType.ULIST, block_type2)

    def test_bad_u_list(self):
        bad_ulist1 = "-This list is missing a space"
        bad_ulist2 = "- This list is\nMissing a - in the second line"
        bad_ulist3 = "This list is\n- Missing a - in the first line"
        bad_ulist4 = "- This list is\n-Missing the space on line 2"
        block_type1 = block_to_block_type(bad_ulist1)
        block_type2 = block_to_block_type(bad_ulist2)
        block_type3 = block_to_block_type(bad_ulist3)
        block_type4 = block_to_block_type(bad_ulist4)
        self.assertNotEqual(BlockType.ULIST, block_type1)
        self.assertNotEqual(BlockType.ULIST, block_type2)
        self.assertNotEqual(BlockType.ULIST, block_type3)
        self.assertNotEqual(BlockType.ULIST, block_type4)

    def test_o_list(self):
        olist1 = "1. This is an o list"
        olist2 = "1. This is an o list\n2. With multiple lines"
        block_type1 = block_to_block_type(olist1)
        block_type2 = block_to_block_type(olist2)
        self.assertEqual(BlockType.OLIST, block_type1)
        self.assertEqual(BlockType.OLIST, block_type2)

    def test_bad_o_list(self):
        bad_olist1 = "2. This o list doesn't start at 1"
        bad_olist2 = "1. This o list\nIs missing the second number"
        bad_olist3 = "This o list\n 2. Is missing the first number"
        bad_olist4 = "1.This o list is missing a space"
        block_type1 = block_to_block_type(bad_olist1)
        block_type2 = block_to_block_type(bad_olist2)
        block_type3 = block_to_block_type(bad_olist3)
        block_type4 = block_to_block_type(bad_olist4)
        self.assertNotEqual(BlockType.OLIST, block_type1)
        self.assertNotEqual(BlockType.OLIST, block_type2)
        self.assertNotEqual(BlockType.OLIST, block_type3)
        self.assertNotEqual(BlockType.OLIST, block_type4)

    def test_paragraph(self):
        paragraph1 = "This is a paragraph"
        paragraph2 = "This is a pragraph\nWith 2 lines"
        block_type1 = block_to_block_type(paragraph1)
        block_type2 = block_to_block_type(paragraph2)
        self.assertEqual(BlockType.PARAGRAPH, block_type1)
        self.assertEqual(BlockType.PARAGRAPH, block_type2)

    # Markdown to HTML Node tests

    def test_paragraphs(self):
        md = "This is a paragraph\n"
        md += "that spans multiple lines\n"
        md += "but has no inlines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is a paragraph that spans multiple lines but has no inlines</p></div>"
        self.assertEqual(expected, html)

    def test_paragraphs_with_inlines(self):
        md = "This is a **bolded** paragraph\n"
        md += "text in a p\n"
        md += "tag here\n\n"
        md += "This is another paragraph with _italic_ and `code` here\n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is a <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> and <code>code</code> here</p></div>"
        self.assertEqual(expected, html)

    def test_codeblock(self):
        md = "```\n"
        md += "This is text that _should_ remain\n"
        md += "the **same** even with inline stuff\n"
        md += "```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        self.assertEqual(expected, html)

    def test_quoteblock(self):
        md = ">This is a quote\n"
        md += "> that spans multiple\n"
        md += "> lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote that spans multiple lines</blockquote></div>"
        self.assertEqual(expected, html)

    def test_quoteblock_with_inlines(self):
        md = ">This is a `code` quote\n"
        md += "> that also has **bold**\n"
        md += "> and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a <code>code</code> quote that also has <b>bold</b> and <i>italic</i></blockquote></div>"
        self.assertEqual(expected, html)

    def test_ulist_block(self):
        md = "- This is item 1\n"
        md += "- This is item 2\n"
        md += "- This is item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>This is item 1</li><li>This is item 2</li><li>This is item 3</li></ul></div>"
        self.assertEqual(expected, html)

    def test_ulist_block_with_inlines(self):
        md = "- This has **bold**\n"
        md += "- This has _italic_\n"
        md += "- This has `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>This has <b>bold</b></li><li>This has <i>italic</i></li><li>This has <code>code</code></li></ul></div>"
        self.assertEqual(expected, html)

    def test_olist_block(self):
        md = "1. This is item 1\n"
        md += "2. This is item 2\n"
        md += "3. This is item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>This is item 1</li><li>This is item 2</li><li>This is item 3</li></ol></div>"
        self.assertEqual(expected, html)

    def test_olist_block_with_inlines(self):
        md = "1. This has **bold**\n"
        md += "2. This has _italic_\n"
        md += "3. This has `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>This has <b>bold</b></li><li>This has <i>italic</i></li><li>This has <code>code</code></li></ol></div>"
        self.assertEqual(expected, html)

    def test_heading_block(self):
        md = [
            "# This is heading 1",
            "## This is heading 2",
            "### This is heading 3",
            "#### This is heading 4",
            "##### This is heading 5",
            "###### This is heading 6",
        ]
        for index in range(len(md)):
            node = markdown_to_html_node(md[index])
            html = node.to_html()
            expected = f"<div><h{index+1}>This is heading {index+1}</h{index+1}></div>"
            self.assertEqual(expected, html)

    def test_heading_block_with_inlines(self):
        md1 = "# This is a `code` heading"
        md2 = "## This is a **bold** heading"
        md3 = "### This is an _italic_ heading"
        node1 = markdown_to_html_node(md1)
        node2 = markdown_to_html_node(md2)
        node3 = markdown_to_html_node(md3)
        html1 = node1.to_html()
        html2 = node2.to_html()
        html3 = node3.to_html()
        expected1 = "<div><h1>This is a <code>code</code> heading</h1></div>"
        expected2 = "<div><h2>This is a <b>bold</b> heading</h2></div>"
        expected3 = "<div><h3>This is an <i>italic</i> heading</h3></div>"
        self.assertEqual(expected1, html1)
        self.assertEqual(expected2, html2)
        self.assertEqual(expected3, html3)
