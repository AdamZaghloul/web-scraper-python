import unittest
from crawl import *


class TestCrawl(unittest.TestCase):
        def test_normalize_url(self):
                input_url = "https://www.boot.dev/blog/path/"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
        def test_normalize_url2(self):
                input_url = "https://www.boot.dev/blog/path"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
        def test_normalize_url3(self):
                input_url = "http://www.boot.dev/blog/path/"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)
        def test_normalize_url4(self):
                input_url = "http://www.boot.dev/blog/path"
                actual = normalize_url(input_url)
                expected = "www.boot.dev/blog/path"
                self.assertEqual(actual, expected)

        def test_heading_from_html(self):
                input_body = "<html><body><h1>Test Title</h1></body></html>"
                actual = get_heading_from_html(input_body)
                expected = "Test Title"
                self.assertEqual(actual, expected)
        def test_heading_from_html2(self):
                input_body = "<html><body><h2>Test Title</h2></body></html>"
                actual = get_heading_from_html(input_body)
                expected = "Test Title"
                self.assertEqual(actual, expected)
        def test_heading_from_html3(self):
                input_body = "<html><body><h1>Test Title</h1><h1>Bad Title</h1></body></html>"
                actual = get_heading_from_html(input_body)
                expected = "Test Title"
                self.assertEqual(actual, expected)
        def test_heading_from_html4(self):
                input_body = "<html><body><p>Test Title</p></body></html>"
                actual = get_heading_from_html(input_body)
                expected = ""
                self.assertEqual(actual, expected)

        def test_get_first_paragraph_from_html_main_priority(self):
                input_body = """<html><body>
                        <p>Outside paragraph.</p>
                        <main>
                        <p>Main paragraph.</p>
                        </main>
                </body></html>"""
                actual = get_first_paragraph_from_html(input_body)
                expected = "Main paragraph."
                self.assertEqual(actual, expected)

        def test_get_first_paragraph_from_html_main_priority2(self):
                        input_body = """<html><body>
                                <p>Outside paragraph.</p>
                                <p>Main paragraph.</p>
                        </body></html>"""
                        actual = get_first_paragraph_from_html(input_body)
                        expected = "Outside paragraph."
                        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()