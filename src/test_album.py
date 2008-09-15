import unittest
import sys

sys.path.append('../')
import api
import album

apikey = "152a230561e72192b8b0f3e42362c6ff"

class testAlbum(unittest.TestCase):
    """ A test class for the Album module. """
    
    def setUp(self):
        self.api_test = api.Api(apikey)
        self.album_test = self.api_test.getAlbum("Oasis", "Supersonic")

    def testAlbumName(self):
        self.assertEqual(self.album_test.name, "Supersonic")

    def testAlbumArtist(self):
        self.assertEqual(self.album_test.artist.name, "Oasis")
        
if __name__ == '__main__':
    unittest.main()
