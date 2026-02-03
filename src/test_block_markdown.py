import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "Just one paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph"])

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_multiple_blank_lines(self):
        md = "block one\n\n\n\nblock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["block one", "block two"])

    def test_leading_trailing_whitespace_on_blocks(self):
        md = "  block one  \n\n  block two  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["block one", "block two"])

    def test_leading_blank_lines(self):
        md = "\n\n\nfirst block\n\nsecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["first block", "second block"])

    def test_trailing_blank_lines(self):
        md = "first block\n\nsecond block\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["first block", "second block"])

    def test_single_newlines_preserved(self):
        md = "line one\nline two\nline three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["line one\nline two\nline three"])

    def test_code_block(self):
        md = "```\ncode here\n```\n\nparagraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```\ncode here\n```", "paragraph"])

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\nparagraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading 1", "## Heading 2", "paragraph"])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h2(self):
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_7_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

    def test_code_block_single_line(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)

    def test_code_block_no_end_is_paragraph(self):
        self.assertEqual(block_to_block_type("```\ncode here"), BlockType.PARAGRAPH)

    def test_code_block_no_start_is_paragraph(self):
        self.assertEqual(block_to_block_type("code here\n```"), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> quote with space"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type(">line one\n>line two\n>line three"), BlockType.QUOTE)

    def test_quote_missing_on_one_line_is_paragraph(self):
        self.assertEqual(block_to_block_type(">line one\nline two\n>line three"), BlockType.PARAGRAPH)

    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple(self):
        self.assertEqual(block_to_block_type("- item one\n- item two\n- item three"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_unordered_list_one_line_invalid_is_paragraph(self):
        self.assertEqual(block_to_block_type("- item one\nitem two\n- item three"), BlockType.PARAGRAPH)

    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple(self):
        self.assertEqual(block_to_block_type("1. one\n2. two\n3. three"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        self.assertEqual(block_to_block_type("2. one\n3. two\n4. three"), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_sequence_is_paragraph(self):
        self.assertEqual(block_to_block_type("1. one\n3. two\n4. three"), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("1.no space"), BlockType.PARAGRAPH)

    def test_paragraph_plain(self):
        self.assertEqual(block_to_block_type("Just some text"), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)

if __name__ == 'main':
    unittest.main()