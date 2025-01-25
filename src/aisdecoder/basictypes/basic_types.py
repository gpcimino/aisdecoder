
class Point:
    def __init__(self, lon: float, lat: float):
        self.lon : float = lon
        self.lat : float = lat

    def __str__(self):
        return f"({self.lat}, {self.lon})"
    
    def as_csv(self):
        return f"{self.lon},{self.lat}"
    
    def as_lat_lon_tuple(self) -> tuple:
        return (self.lat, self.lon)
    
    def has_valid_latitude(self) -> bool:
        return -90 <= self.lat <= 90
    
    def has_valid_longitude(self) -> bool:
        return -180 <= self.lon <= 180

class Rectangle:
    def __init__(self, min_lon, min_lat, max_lon, max_lat) -> None:
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat

    def lon_size(self) -> float:
        return self.max_lon - self.min_lon
      
    def lat_size(self) -> float:
        return self.max_lat - self.min_lat

    def contains(self, point: Point):
        return self.min_lon <= point.lon <= self.max_lon and self.min_lat <= point.lat <= self.max_lat


class Grid:
    def __init__(self, bbox, lon_cell_size, lat_cell_size):
        self.bbox = bbox
        self.lon_cell_size = lon_cell_size
        self.lat_cell_size= lat_cell_size

    def size(self) -> tuple[int, int]:
        return (self.lon_num_cells(), self.lat_num_cells())
        
    def lat_num_cells(self) -> int:
        # if self.bbox.lat_size() % self.lat_cell_size != 0:
        #     raise ValueError("Latitude size is not divisible by grid size")
        return int(self.bbox.lat_size() / self.lat_cell_size)
    

    def lon_num_cells(self) -> int:
        # if Decimal(self.bbox.lon_size()) % Decimal(self.lon_cell_size) != 0:
        #     raise ValueError("Longitude size is not divisible by grid size")
        return int(self.bbox.lon_size() / self.lon_cell_size)    

    # def lat_coords(self):
    #     return np.linspace(self.bbox.min_lat, self.bbox.max_lat, num=self.lat_num_cells(), endpoint=True)    
    
    # def lon_coords(self):
    #     return np.linspace(self.bbox.min_lon, self.bbox.max_lon, num=self.lon_num_cells(), endpoint=True)