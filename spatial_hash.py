# Spatial_Hash Class
#

from settings import COLLISION_CELL_SIZE

class spatial_hash:
    def __init__(self, cell_size = COLLISION_CELL_SIZE):
        self.cell_size = cell_size
        self.buckets = {}

    def _get_bucket_keys(self, x, y):
        """Return keys for the buckets that the point might belong to."""
        cell_x = int(x / self.cell_size)
        cell_y = int(y / self.cell_size)
        return [
            (cell_x, cell_y),
            (cell_x + 1, cell_y),
            (cell_x, cell_y + 1),
            (cell_x + 1, cell_y + 1)
        ]

    def insert(self, blob):
        for key in self._get_bucket_keys(blob.x, blob.y):
            if key not in self.buckets:
                self.buckets[key] = []
            self.buckets[key].append(blob)

    def potential_collisions(self, blob):
        """Get a list of blobs that are potentially colliding with the given blob."""
        nearby_blobs = set()
        for key in self._get_bucket_keys(blob.x, blob.y):
            nearby_blobs.update(self.buckets.get(key, []))
        return nearby_blobs - {blob}
