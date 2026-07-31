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

        def test_get_urls_from_html_absolute(self):
                input_url = "https://crawler-test.com"
                input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
                actual = get_urls_from_html(input_body, input_url)
                expected = ["https://crawler-test.com"]
                self.assertEqual(actual, expected)
        def test_get_images_from_html_relative(self):
                input_url = "https://crawler-test.com"
                input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
                actual = get_images_from_html(input_body, input_url)
                expected = ["https://crawler-test.com/logo.png"]
                self.assertEqual(actual, expected)

        def test_extract_page_data_basic(self):
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                        <h1>Test Title</h1>
                        <p>This is the first paragraph.</p>
                        <a href="/link1">Link 1</a>
                        <img src="/image1.jpg" alt="Image 1">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                        "url": "https://crawler-test.com",
                        "heading": "Test Title",
                        "first_paragraph": "This is the first paragraph.",
                        "outgoing_links": ["https://crawler-test.com/link1"],
                        "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
                self.assertEqual(actual, expected)

        def test_extract_page_data_basic2(self):
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                        <h1>Test Title2</h1>
                        <p>This is the first paragraph2.</p>
                        <a href="/link2">Link 2</a>
                        <img src="/image2.jpg" alt="Image 1">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                        "url": "https://crawler-test.com",
                        "heading": "Test Title2",
                        "first_paragraph": "This is the first paragraph2.",
                        "outgoing_links": ["https://crawler-test.com/link2"],
                        "image_urls": ["https://crawler-test.com/image2.jpg"],
                }
                self.assertEqual(actual, expected)

        def test_extract_page_data_basic3(self):
                input_url = "https://crawler-test.com"
                input_body = """<html><body>
                        <h1>This is the Title</h1>
                        <p>This is the first paragraph</p>
                        <a href="/link2">Link 2</a>
                        <img src="/image2.jpg" alt="Image 1">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                        "url": "https://crawler-test.com",
                        "heading": "This is the Title",
                        "first_paragraph": "This is the first paragraph",
                        "outgoing_links": ["https://crawler-test.com/link2"],
                        "image_urls": ["https://crawler-test.com/image2.jpg"],
                }
                self.assertEqual(actual, expected)
        def test_extract_recipe_data_complex(self):
                input_url = "https://cooking-example.com/recipes"
                input_body = """<html><body>
                        <h1>Grandma's Stew</h1>
                        <p>First paragraph.</p>
                        <p>Second paragraph, ignored.</p>
                        <a href="https://external-site.com/other-recipe">External Recipe</a>
                        <a href="/recipes/soup">Soup</a>
                        <img src="https://cdn.example.com/stew.jpg" alt="Stew">
                        <img src="/images/bowl.png" alt="Bowl">
                </body></html>"""
                actual = extract_page_data(input_body, input_url)
                expected = {
                        "url": "https://cooking-example.com/recipes",
                        "heading": "Grandma's Stew",
                        "first_paragraph": "First paragraph.",
                        "outgoing_links": [
                        "https://external-site.com/other-recipe",
                        "https://cooking-example.com/recipes/soup",
                        ],
                        "image_urls": [
                        "https://cdn.example.com/stew.jpg",
                        "https://cooking-example.com/images/bowl.png",
                        ],
                }
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()