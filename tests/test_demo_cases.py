"""Regression tests for versioned, reproducible before/after artifacts."""
import importlib.util
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'examples' / 'cases'

class SectionsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            self.ids.append(dict(attrs).get('id'))

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class ReproducibleCaseTests(unittest.TestCase):
    def test_ui_failure_and_fixed_behavior(self):
        before = (CASES/'ui/before.html').read_text(encoding='utf8')
        after = (CASES/'ui/after.html').read_text(encoding='utf8')
        p1, p2 = SectionsParser(), SectionsParser()
        p1.feed(before); p2.feed(after)
        self.assertEqual(p1.ids, ['hero', 'features', 'testimonials'])
        self.assertEqual(p2.ids, ['hero', 'features'])
        self.assertIn('background:#101521', before)
        self.assertIn('background:#ffffff', after)
        self.assertIn('href="/produtos"', after)
    def test_code_failure_and_fixed_behavior(self):
        before = load_module(CASES/'code/before.py', 'before_sort')
        after = load_module(CASES/'code/after.py', 'after_sort')
        values = ['11.00', '2.50', '3.00', '2.50']
        expected = ['2.50','2.50','3.00','11.00']
        self.assertNotEqual(before.sort_prices(values), expected)
        self.assertEqual(after.sort_prices(values), expected)
    def test_text_failure_and_fixed_behavior(self):
        before = (CASES/'text/before.md').read_text(encoding='utf8').casefold()
        after = (CASES/'text/after.md').read_text(encoding='utf8').casefold()
        self.assertIn('elimina 100%', before)
        self.assertNotIn('elimina 100%', after)
        self.assertIn('autorização explícita', after)
        self.assertIn('não garante', after)

if __name__ == '__main__':
    unittest.main()
