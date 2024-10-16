import os
from scrapy.extensions.feedexport import FileFeedStorage

class CustomFileFeedStorage(FileFeedStorage):
    """
    Een aangepaste File Feed Storage extensie die bestaande bestanden overschrijft.
    """

    def open(self, spider):
        """Return het geopende bestand."""
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        # Wijzig 'ab' (append) naar 'wb' (write) om het bestand te overschrijven
        return open(self.path, 'wb')
