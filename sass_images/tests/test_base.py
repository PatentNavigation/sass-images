from __future__ import unicode_literals

import os.path
from six import StringIO
import unittest
from sass_images import (
    get_variable_from_path,
    get_image_dimensions,
    get_image_mimetype,
    get_image_url,
    generate_sass_from_dir)


class BaseTest(unittest.TestCase):
    def _file_path(self, filename):
        return os.path.join(os.path.dirname(__file__), 'files', filename)

    def _test_variable_names(self, root):
        t = get_variable_from_path
        join = os.path.join

        self.assertEqual(t(root, join(root, "simple.png")), "$img-simple")
        self.assertEqual(t(root, join(root, "dir/simple.png")), "$img-dir-simple")
        self.assertEqual(t(root, join(root, "dir/dashed-name.png")), "$img-dir-dashed-name")
        self.assertEqual(t(root, join(root, "underscored_name.png")), "$img-underscored-name")
        self.assertEqual(t(root, join(root, "numbers1234.png")), "$img-numbers1234")
        self.assertEqual(t(root, join(root, "Foo/Lower-Cased-Name.png")), "$img-foo-lower-cased-name")
        self.assertEqual(t(root, join(root, "Foo/File With Spaces.png")), "$img-foo-file-with-spaces")

    def test_unslashed_root(self):
        self._test_variable_names("../web/static/img")

    def test_slashed_root(self):
        self._test_variable_names("../web/static/img/")

    def test_get_image_dimensions(self):
        t = get_image_dimensions

        self.assertEqual(t(self._file_path('86px-Nikola_Tesla.jpg')), (86, 120))

    def test_get_image_mimetype(self):
        t = get_image_mimetype

        self.assertEqual(t(self._file_path('86px-Nikola_Tesla.jpg')), 'image/jpeg')
        self.assertEqual(t(self._file_path('95px-Benjamin_Franklin.png')), 'image/png')
        self.assertEqual(t(self._file_path('spinner.gif')), 'image/gif')

    def test_get_image_url(self):
        result = get_image_url(self._file_path('86px-Nikola_Tesla.jpg'), '', 4000)
        self.assertTrue(result.startswith("url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE"),
                        "URL is {}".format(result))

        # Above the threshold, it generates a URL
        result = get_image_url(self._file_path('86px-Nikola_Tesla.jpg'),
                               'img/86px-Nikola_Tesla.jpg', 1000)
        self.assertEqual(result, "url('img/86px-Nikola_Tesla.jpg')")

    def test_generate_sass_from_dir(self):
        self.maxDiff = None
        result = StringIO()
        dir = os.path.join(os.path.dirname(__file__), 'files')

        # Test generating all image URLs
        generate_sass_from_dir(dir, result, 0, 'files/', False)

        RESULT = """// files/120px-Thomas_Edison2-crop.jpg
$img-120px-thomas-edison2-crop-url: url('files/120px-Thomas_Edison2-crop.jpg');
$img-120px-thomas-edison2-crop-width: 120px;
$img-120px-thomas-edison2-crop-height: 150px;

// files/86px-Nikola_Tesla.jpg
$img-86px-nikola-tesla-url: url('files/86px-Nikola_Tesla.jpg');
$img-86px-nikola-tesla-width: 86px;
$img-86px-nikola-tesla-height: 120px;

// files/95px-Benjamin_Franklin.png
$img-95px-benjamin-franklin-url: url('files/95px-Benjamin_Franklin.png');
$img-95px-benjamin-franklin-width: 95px;
$img-95px-benjamin-franklin-height: 119px;

// files/96px-Tesla2.jpg
$img-96px-tesla2-url: url('files/96px-Tesla2.jpg');
$img-96px-tesla2-width: 96px;
$img-96px-tesla2-height: 120px;

// files/spinner.gif
$img-spinner-url: url('files/spinner.gif');
$img-spinner-width: 24px;
$img-spinner-height: 24px;

"""
        self.assertEqual(result.getvalue(), RESULT)
