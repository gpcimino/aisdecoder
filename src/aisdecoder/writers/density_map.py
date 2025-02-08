# type: ignore

import matplotlib.pyplot as plt
import numpy as np

from aisdecoder.basictypes.basic_types import Rectangle
from aisdecoder.writers.writer import Writer

from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_kinematic_message import AISKinematicMessage
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_message_5 import AISMessage5
    from aisdecoder.ais_message_18 import AISMessage18
    from aisdecoder.ais_message_19 import AISMessage19   
    from aisdecoder.filters.filter import Filter 

class DensityMap(Writer):
    def __init__(self, 
            map_boundaries: Rectangle,
            output_file="density_map.png", 
            grid_size=(500, 450), 
            filters: Optional[List["Filter"]]=None
        ):
        super().__init__(filters)
        self._map_boundaries = map_boundaries
        self.output_file = output_file
        self.grid_size = grid_size
        self.data = []  # To store (latitude, longitude) tuples

    def write_message123(self, message: "AISMessage123") -> None:
        if self.filters_match(message):
            self.add_message(message)

    def write_message5(self, message: "AISMessage5") -> None:
        pass


    def write_message18(self, message: "AISMessage18") -> None:
        if self.filters_match(message):
            self.add_message(message)

    def write_message19(self, message: "AISMessage19") -> None:
        if self.filters_match(message):
            self.add_message(message)                  

    def add_message(self, message: "AISKinematicMessage" ):
        if message.is_kinematic() and message.is_inside(self._map_boundaries):
            self.data.append(message.position().as_lat_lon_tuple())
            if len(self.data)%10000 == 0:
                print(len(self.data))
        

    def generate_density_map(self):
        """Generate a simplified density map (heatmap) and save it as a PNG file."""
        if not self.data:
            print("No data to process!")
            return

        # Convert data to a numpy array
        data = np.array(self.data)

        # Create a 2D histogram
        latitudes = data[:, 0]
        longitudes = data[:, 1]
        heatmap, xedges, yedges = np.histogram2d(longitudes, latitudes, bins=self.grid_size)

        # Normalize the histogram for better visualization
        #heatmap = heatmap / heatmap.max()
        heatmap = np.log(heatmap)

        # Plot the density map
        plt.figure(figsize=(10, 8))
        plt.imshow(heatmap.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', cmap='hot', aspect='auto')
        plt.colorbar(label="Density")
        plt.title("Density Map")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        # Save the image as a PNG file
        plt.savefig(self.output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Density map saved as {self.output_file}")

