import typing
import os
import json
from .Items import item_table, cannon_item_table, SM64Item
from .Locations import location_table, SM64Location
from .Options import sm64_options
from .Rules import set_rules
from .Regions import create_regions, sm64courses, sm64entrances_s, sm64_internalloc_to_string, sm64_internalloc_to_regionid
from BaseClasses import Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld

class SM64Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up SM64EX for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing"]
    )]


class SM64World(World):
    """ 
    The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons,
    combined with traditional Mario gameplay, visual style, and characters.
    """

    game: str = "Super Mario 64"
    topology_present = False

    web = SM64Web()

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 7
    required_client_version = (0, 3, 0)

    area_connections: typing.Dict[int, int]

    option_definitions = sm64_options

    def generate_early(self):
        self.topology_present = self.world.AreaRandomizer[self.player].value

    def create_regions(self):
        create_regions(self.world,self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.world, self.player, self.area_connections)
        if self.topology_present:
            # Write area_connections to spoiler log
            for entrance, destination in self.area_connections.items():
                self.world.spoiler.set_entrance(
                    sm64_internalloc_to_string[entrance] + " Entrance",
                    sm64_internalloc_to_string[destination],
                    'entrance', self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "1Up Mushroom":
            classification = ItemClassification.filler
        elif name == "Power Star":
            classification = ItemClassification.progression_skip_balancing
        else:
            classification = ItemClassification.progression
        item = SM64Item(name, classification, item_id, self.player)

        return item

    def generate_basic(self):
        starcount = self.world.AmountOfStars[self.player].value
        if (not self.world.EnableCoinStars[self.player].value):
            starcount = max(35,self.world.AmountOfStars[self.player].value-15)
        starcount = max(starcount, self.world.FirstBowserStarDoorCost[self.player].value, 
                        self.world.BasementStarDoorCost[self.player].value, self.world.SecondFloorStarDoorCost[self.player].value,
                        self.world.MIPS1Cost[self.player].value, self.world.MIPS2Cost[self.player].value,
                        self.world.StarsToFinish[self.player].value)
        self.world.itempool += [self.create_item("Power Star") for i in range(0,starcount)]
        self.world.itempool += [self.create_item("1Up Mushroom") for i in range(starcount,120 - (15 if not self.world.EnableCoinStars[self.player].value else 0))]

        if (not self.world.ProgressiveKeys[self.player].value):
            key1 = self.create_item("Basement Key")
            key2 = self.create_item("Second Floor Key")
            self.world.itempool += [key1,key2]
        else:
            self.world.itempool += [self.create_item("Progressive Key") for i in range(0,2)]

        wingcap = self.create_item("Wing Cap")
        metalcap = self.create_item("Metal Cap")
        vanishcap = self.create_item("Vanish Cap")
        self.world.itempool += [wingcap,metalcap,vanishcap]

        if (self.world.BuddyChecks[self.player].value):
            self.world.itempool += [self.create_item(name) for name, id in cannon_item_table.items()]
        else:
            self.world.get_location("BoB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock BoB"))
            self.world.get_location("WF: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WF"))
            self.world.get_location("JRB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock JRB"))
            self.world.get_location("CCM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock CCM"))
            self.world.get_location("SSL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SSL"))
            self.world.get_location("SL: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock SL"))
            self.world.get_location("WDW: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock WDW"))
            self.world.get_location("TTM: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock TTM"))
            self.world.get_location("THI: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock THI"))
            self.world.get_location("RR: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock RR"))

        if (self.world.ExclamationBoxes[self.player].value > 0):
            self.world.itempool += [self.create_item("1Up Mushroom") for i in range(0,29)]
        else:
            self.world.get_location("CCM: 1Up Block Near Snowman", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("CCM: 1Up Block Ice Pillar", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("CCM: 1Up Block Secret Slide", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("BBH: 1Up Block Top of Mansion", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("HMC: 1Up Block above Pit", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("HMC: 1Up Block Past Rolling Rocks", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("SSL: 1Up Block Outside Pyramid", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("SSL: 1Up Block Pyramid Left Path", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("SSL: 1Up Block Pyramid Back", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("SL: 1Up Block Near Moneybags", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("SL: 1Up Block inside Igloo", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("WDW: 1Up Block in Downtown", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("TTM: 1Up Block on Red Mushroom", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("THI: 1Up Block THI Small near Start", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("THI: 1Up Block THI Large near Start", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("THI: 1Up Block Windy Area", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("TTC: 1Up Block Midway Up", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("TTC: 1Up Block at the Top", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("RR: 1Up Block Top of Red Coin Maze", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("RR: 1Up Block Under Fly Guy", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("RR: 1Up Block On House in the Sky", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Bowser in the Dark World 1Up Block on Tower", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Bowser in the Dark World 1Up Block near Goombas", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Cavern of the Metal Cap 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Vanish Cap Under the Moat 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Bowser in the Fire Sea 1Up Block Swaying Stairs", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Bowser in the Fire Sea 1Up Block Near Poles", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Wing Mario Over the Rainbow 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.world.get_location("Bowser in the Sky 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))

    def get_filler_item_name(self) -> str:
        return "1Up Mushroom"

    def fill_slot_data(self):
        return {
            "AreaRando": self.area_connections,
            "FirstBowserDoorCost": self.world.FirstBowserStarDoorCost[self.player].value,
            "BasementDoorCost": self.world.BasementStarDoorCost[self.player].value,
            "SecondFloorDoorCost": self.world.SecondFloorStarDoorCost[self.player].value,
            "MIPS1Cost": self.world.MIPS1Cost[self.player].value,
            "MIPS2Cost": self.world.MIPS2Cost[self.player].value,
            "StarsToFinish": self.world.StarsToFinish[self.player].value,
            "DeathLink": self.world.death_link[self.player].value,
        }

    def generate_output(self, output_directory: str):
        if self.world.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.world.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_file_safe_player_name(self.player)}.apsm64ex"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def modify_multidata(self, multidata):
        if self.topology_present:
            er_hint_data = {}
            for entrance, destination in self.area_connections.items():
                regionid = sm64_internalloc_to_regionid[destination]
                region = self.world.get_region(sm64courses[regionid], self.player)
                for location in region.locations:
                    er_hint_data[location.address] = sm64_internalloc_to_string[entrance]
            multidata['er_hint_data'][self.player] = er_hint_data
