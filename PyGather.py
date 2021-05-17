import requests
import json
import base64

class API:
    """
    Class that handles interaction with the Gather http API

    To learn more about the Gather http API visit https://www.notion.so/EXTERNAL-Gather-http-API-3bbf6c59325f40aca7ef5ce14c677444

    Attributes:
        API_KEY (str): API Key
        SPACE_ID (str): Space ID
    """

    def __init__(self, _api_key: str, _space_id: str):
        """
        Creates an instance of the GatherTownAPI class
        
        Args:
            _api_key (str): API Key
        """

        self.API_KEY = _api_key
        self.SPACE_ID = _space_id
        self.URL = "https://gather.town/api"

    def create_room(self):
        return None

    def get_map(self, map_id: str):
        """
        Calls the Gather HTTP API to get a map's data and returns a GatherTownObject

        Args:
            map_id (str): Map ID, usually the name of the map

        Returns:
            GatherTownMap object
        """
        payload = {"apiKey": self.API_KEY, "spaceId": self.SPACE_ID, "mapId": map_id}
        get_map_raw = requests.get(self.URL + "/getMap", params=payload)
        get_map = get_map_raw.json()
        
        map_id = get_map["id"]
        map_bg = get_map["backgroundImagePath"]
        map_assets = get_map["assets"]
        map_announcer = get_map["announcer"]
        map_objects = [] # Objects list are empty, will be filled after initialising map objects
        map_use_drawn_bg = get_map["useDrawnBG"]
        map_spaces = get_map["spaces"]
        try:
            map_floors = get_map["floors"]
        except:
            map_floors = {}
        map_collisions = get_map["collisions"]
        try:
            map_walls = get_map["walls"]
        except:
            map_walls = {}
        map_portals = get_map["portals"]
        map_spawns = get_map["spawns"]
        map_dimensions = get_map["dimensions"]
        map_parent_space = self.SPACE_ID

        gathertown_map = Map(map_bg, map_assets, map_announcer, 
                                       map_objects, map_use_drawn_bg, map_spaces, 
                                       map_id, map_floors, map_collisions, 
                                       map_walls, map_portals, map_spawns, 
                                       map_dimensions, map_parent_space)

        # We now iterate through each object, init a new GatherTownObject and add it to the gathertown_map.objects list
        for obj in get_map["objects"]:
            obj_name = obj.get("_name", "no_name_included")
            obj_scale = obj.get("scale")
            obj_x = obj.get("x")
            obj_y = obj.get("y")
            obj_height = obj.get("height")
            obj_width = obj.get("width")
            obj_normal = obj.get("normal")
            obj_highlighted = obj.get("highlighted")
            obj_type = obj.get("type")
            obj_properties = obj.get("properties")
            obj_parent_map = gathertown_map
            try:
                sound_properties = obj.get("sound")
                obj_sound_properties = ObjectSoundProperties(sound_properties.get("volume"),
                                                             sound_properties.get("maxDistance"),
                                                             sound_properties.get("src"),
                                                             sound_properties.get("loop"))
            except:
                obj_sound_properties = None

            x = Object(obj_name, obj_scale, obj_x, 
                                 obj_y, obj_height, obj_width, 
                                 obj_normal, obj_highlighted, obj_type, 
                                 obj_properties, obj_parent_map,
                                 obj_sound_properties)

            gathertown_map.objects.append(x)
        
        return gathertown_map

    def set_map(self, map_instance) -> int:
        """
        Calls the Gather HTTP API to get a map's data and returns a GatherTownObject

        Args:
            map_instance (GatherTownMap): An instance of GatherTownmap

        Returns:
            Status code reply of the request
        """
        headers = {'Content-Type': 'application/json'}
        payload = {
            "apiKey": self.API_KEY, 
            "spaceId": self.SPACE_ID, 
            "mapId": map_instance.id, 
            "mapContent": map_instance.get_dict()
        }
        set_map = requests.request("POST",
                                   self.URL + "/setMap", 
                                   headers = headers,
                                   data=json.dumps(payload)
                                   )
        
        return set_map.status_code

    def get_email_guestlist(self):
        return None

    def set_email_guestlist(self):
        return None

class Base64HexArray:
    """
    Class that represents a Base64 Hexadecimal array
    These arrays are used in the GatherTownMap data to represent positions of collisions, walls, floors etc...
    """

    def __init__(self, _hex_array_base64: str, _parent_map):
        self.hex_array_base64 = _hex_array_base64
        self.parent_map = _parent_map

    def get_byte_array(self):
        hex_array_base64_bytes = self.hex_array_base64.encode('ascii')
        hex_array_bytes = base64.b64decode(hex_array_base64_bytes)

        return bytearray(hex_array_bytes)

    def set_byte_array(self, new_array: bytearray):
        hex_array_encoded_data = base64.b64encode(new_array)
        self.hex_array_base64 = hex_array_encoded_data.decode('ascii')

    def set_value_at_location(self, x: int, y: int, isTrue: bool):
        position = x + (y * self.parent_map.dimensions[0])
        print("Position: " + str(position))
        byte_array = self.get_byte_array()
        print("Byte Array length: " + str(len(byte_array)))
        print("Original value is " + str(byte_array[position]))

        if isTrue:
            byte_array[position] = 1
        else:
            byte_array[position] = 0

        print("New value is " + str(byte_array[position]))

        self.set_byte_array(byte_array)

class Map:
    """
    Class that represents a GatherTown Map

    Attributes:
        background_image (str): 
        assets (list): 
        announcer (list):
        objects (list):
        use_drawn_bg (bool):
        spaces (list): 
        id (str): 
        floors (dict): 
        collisions (str): 
        walls (dict): 
        portals (list):
        spawns (list):
        dimensions (list): 
        parent_space (str):
    """

    def __init__(self, _background_image: str, _assets: list, 
                 _announcer: list, _objects: list, _use_drawn_bg: bool, 
                 _spaces: list, _id: str, _floors: dict, 
                 _collisions: Base64HexArray, _walls: dict, _portals: list, 
                 _spawns: list, _dimensions: list, _parent_space: str):
        """
        Creates an instance of the GatherTownMap class

        Args:
            _background_image (str): 
            _assets (list): 
            _announcer (list):
            _objects (list):
            _use_drawn_bg (bool):
            _spaces (list): 
            _id (str): 
            _floors (dict): 
            _collisions (GatherTownBase64HexArray): 
            _walls (dict): 
            _portals (list):
            _spawns (list):
            _dimensions (list): 
            _parent_space (str):
        """
        self.id = _id
        self.background_image = _background_image
        self.assets = _assets
        self.announcer = _announcer
        self.objects = _objects
        self.use_drawn_bg = _use_drawn_bg
        self.spaces = _spaces
        self.floors = _floors
        self.collisions = Base64HexArray(_collisions, self)
        self.walls = _walls
        self.portals = _portals
        self.spawns = _spawns
        self.dimensions = _dimensions
        self.parent_space = _parent_space

    def update_map(self, _gathertown_api: API):
        return None

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        for item in self.objects:
            if item.name == obj.name:
                if item.has_collision == True:
                    item.set_tile_collision(False)
                index = self.objects.index(item)
                self.objects.pop(index)

    def remove_object_by_name(self, obj_name):
        for item in self.objects:
            if item.name == obj_name:
                if item.has_collision == True:
                    item.set_tile_collision(False)
                index = self.objects.index(item)
                self.objects.pop(index)

    def get_json(self):
        """
        Get this map as a json string
        """
        map_dict = {
            "backgroundImagePath": self.background_image,
            "assets": self.assets,
            "announcer": self.announcer,
            "objects": [],
            "useDrawnBG": self.use_drawn_bg,
            "spaces": self.spaces,
            "id": self.id,
            "floors": self.floors,
            "collisions": self.collisions.hex_array_base64,
            "walls": self.walls,
            "portals": self.portals,
            "spawns": self.spawns,
            "dimensions": self.dimensions
        }

        for obj in self.objects:
            map_dict["objects"].append(obj.get_json())

        return json.dumps(map_dict)

    def get_dict(self):
        """
        Get this map as a dictionary
        """
        map_dict = {
            "backgroundImagePath": self.background_image,
            "assets": self.assets,
            "announcer": self.announcer,
            "objects": [],
            "useDrawnBG": self.use_drawn_bg,
            "spaces": self.spaces,
            "id": self.id,
            "floors": self.floors,
            "collisions": self.collisions.hex_array_base64,
            "walls": self.walls,
            "portals": self.portals,
            "spawns": self.spawns,
            "dimensions": self.dimensions
        }

        for obj in self.objects:
            map_dict["objects"].append(obj.get_dict())

        return map_dict

class ObjectSoundProperties:
    """
    """

    def __init__(self, volume, max_distance: int, source: str, loop: bool):
        self.volume = volume
        self.max_distance = max_distance
        self.source = source
        self.loop = loop

class Object:
    """
    Class that represents a GatherTown Object
    """

    def __init__(self, _name: str, _scale: float, 
                 _x: int, _y: int, _height: int, _width: int, 
                 _normal: str, _highlighted: str, 
                 _type: int, _properties: dict, _parent_map, 
                 sound_properties: ObjectSoundProperties):
        self.name = _name
        self.scale = _scale
        self.x = _x
        self.y = _y
        self.height = _height
        self.width = _width
        self.normal = _normal
        self.highlighted = _highlighted
        self.type = _type
        self.properties = _properties
        self.parent_map = _parent_map
        self.has_collision = False
        self.sound_properties = sound_properties

    def move_to(self, x, y):
        """
        Move object to new spot

        Args:
            x (int): new X (left/right) coordinate 
            y (int): new Y (up/down) coordinate
        
        """
        if self.has_collision:
            self.set_tile_collision(False)

        self.x = x
        self.y = y

        if self.has_collision:
            self.set_tile_collision(True)

    def move_by(self, x, y):
        """
        Move object by a certain amount of units

        Args:
            x (int): Move object by given amount of units in X (left/right) 
            y (int): Move object by given amount of units in Y (up/down) 
        """
        self.move_to(self.x + x, self.y + y)
        
    def move_left(self, x=1):
        """
        Move object left

        Args:
            x (int): Move object left by this amount of units, by deault one unit
        """
        self.move_to(self.x - x, self.y)
            
    def move_right(self, x=1):
        """
        Move object right

        Args:
            x (int): Move object right by this amount of units, by default one unit
        """
        self.move_to(self.x + x, self.y)

    def move_up(self, y=1):
        """
        Move object up

        Args:
            y (int): Move object up by this amount of units, by default one unit
        """
        self.move_to(self.x, self.y - y)

    def move_down(self, y=1):
        """
        Move object down

        Args:
            y (int): Move object down by this amount of units, by default one unit
        """
        self.move_to(self.x, self.y + y)

    def set_tile_collision(self, has_collision: bool):
        """
        Set object's collision

        Notes on this:

        The collision data of a map is stored in GatherTownMap.collisions as a string. This string is a hex array encoded in 
        BASE64.
        """
        self.has_collision = has_collision

        for height in range(self.height):
            for width in range(self.width):
                self.parent_map.collisions.set_value_at_location(self.x + width, self.y + height, has_collision)

    def get_json(self):
        """
        Get this object as a json string
        """
        object_dict = {
            "_name": self.name,
            "scale": self.scale,
            "x": self.x,
            "y": self.y,
            "height": self.height,
            "width": self.width,
            "normal": self.normal,
            "type": self.type,
            "highlighted": self.highlighted,
            "properties": self.properties
        }
        return json.dumps(object_dict)

    def get_dict(self):
        """
        Get this object as a dictionary
        """
        object_dict = {
            "_name": self.name,
            "scale": self.scale,
            "x": self.x,
            "y": self.y,
            "height": self.height,
            "width": self.width,
            "normal": self.normal,
            "type": self.type,
            "highlighted": self.highlighted,
            "properties": self.properties
        }
        return object_dict

