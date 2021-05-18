import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PyGather

API_KEY = "Insert API key here"
SPACE_NAME = "Insert Space name here"
MAP_NAME = "Insert map name here"

gather_api = PyGather.API(API_KEY, SPACE_NAME)

map = gather_api.get_map(MAP_NAME)

# Creating a new Object instance named table at coordinates 20, 20 with height of 1 and width of 3
# The images are taken from Gather
table = PyGather.Object("table", 1, 20, 20, 1, 3,
                        "https://cdn.gather.town/v0/b/gather-town.appspot.com/o/internal-dashboard-upload%2Fbx28G5ZFHBI7dwB7?alt=media&token=4f42797f-b7c3-4009-bd6f-1047139b974b",
                        "https://cdn.gather.town/v0/b/gather-town.appspot.com/o/internal-dashboard-upload%2Fbx28G5ZFHBI7dwB7?alt=media&token=4f42797f-b7c3-4009-bd6f-1047139b974b",
                        None, {}, map, None)

# Adding table object to the map
map.add_object(table)

# Setting the table collision to be true. This will adjust the map's collision hex array
table.set_tile_collision(True)

# Now we update the map. If all went well, a table will have been spawned at coordinates 20, 20 and will have collision
map.update_map()