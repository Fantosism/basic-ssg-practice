import unittest
from block_markdown import markdown_to_blocks

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

if __name__ == 'main':
    unittest.main()