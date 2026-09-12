#!/usr/bin/env python3

import contextlib
import io
import unittest
from unittest.mock import patch

from src.file_extensions import file_extensions, main


class FileExtensions(unittest.TestCase):

    def test_first(self):
        correct_d = {'txt': ['file1.txt', 'file2.txt'],
                     'pdf': ['mydocument.pdf'],
                     'gz': ['archive.tar.gz']}
        no_extension, d = file_extensions("src/filenames.txt")
        self.assertEqual(
            no_extension, ["test"],
            msg="file_extensions('src/filenames.txt') should report "
            "['test'] as the only filename without an extension. "
            "Got %r." % (no_extension,))
        self.assertEqual(
            d, correct_d,
            msg="file_extensions('src/filenames.txt') returned the wrong "
            "dictionary of files grouped by extension. Got %r, expected "
            "%r." % (d, correct_d))

    def test_calls(self):
        with patch('builtins.open', side_effect=open) as o:
            file_extensions("src/filenames.txt")
            o.assert_called_once()

    def test_main(self):
        with patch('src.file_extensions.file_extensions',
                   side_effect=[([], {})]) as fe:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                main()
            self.assertEqual(
                fe.call_count, 1,
                msg="main() should call file_extensions() exactly once.")
            result = buf.getvalue().strip().split('\n')
            self.assertEqual(
                len(result), 1,
                msg="main() should print exactly one line when there are "
                "no files with a missing extension.")
            self.assertEqual(
                result[0], "0 files with no extension",
                msg="main() printed %r; expected '0 files with no "
                "extension' when file_extensions() reports an empty list "
                "of extensionless files." % (result[0],))


if __name__ == '__main__':
    unittest.main()
