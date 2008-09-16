import unittest
import datetime
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
        
    def testAlbumUrl(self):
        url = 'http://www.last.fm/music/Oasis/Supersonic'
        self.assertEqual(self.album_test.url, url)
        
    def testAlbumReleaseDate(self):
        date = datetime.datetime(1994, 7, 28, 0, 0)
        self.assertEqual(self.album_test.releaseDate, date)
        
    def testAlbumMbid(self):
        mbid = '2c2a24de-67b6-483b-b597-9c6b7891ba90'
        self.assertEqual(self.album_test.mbid, mbid)
        
    def testAlbumId(self):
        id = 2038492
        self.assertEqual(self.album_test.id, id)
    
if __name__ == '__main__':
    unittest.main()
