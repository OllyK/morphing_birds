from .SkeletonDefinition import SkeletonDefinition


class SpiderSkeletonDefinition(SkeletonDefinition):
    """
    The `SpiderSkeletonDefinition` class is a specific implementation of the 
    `SkeletonDefinition` class, tailored to represent the shape of the spider. 
    By extending `SkeletonDefinition`, it inherits 
    all the methods and attributes necessary for defining markers and body 
    sections, while also allowing for customisation specific to spiders.
    """

    def __init__(self):


        leg_marker_names = [
            "claw", 
            "tibiametatarsus",
            "patella",
            "coxa"
        ]
        
        body_marker_names = [
            "clypeus",
            "pedicel",
            "spinneret"
        ]

        fixed_marker_names = [
            "center"
        ]


        # Put the numbers 1 to 8 next to the leg markers. 
        all_leg_marker_names = [f"{marker_name}{i}" for i in range(1, 9) for marker_name in leg_marker_names]

        marker_names = all_leg_marker_names + body_marker_names

        # E.g. leg_1: [claw1, tibiametatarsus1, patella1, coxa1] and so on.
        body_sections = {
            **{f"leg_{ii}": [f"claw{ii}", f"tibiametatarsus{ii}", f"patella{ii}", f"coxa{ii}", f"patella{ii}", f"tibiametatarsus{ii}", f"claw{ii}"] for ii in range(1, 9)},
            "body": ["clypeus","coxa1", "coxa2", "coxa3", "coxa4", "spinneret", "coxa5", "coxa6", "coxa7", "coxa8"]
        }

        super().__init__(marker_names, fixed_marker_names, body_sections)

    def get_all_marker_names(self):
        """
        Returns a list of all marker names from the spider shape definition.
        """
        return self.marker_names + self.fixed_marker_names

    def get_right_marker_names(self):
        """
        Returns a list of all right-side marker names from the spider shape definition.
        """
        # The markers with 1, 2, 3, or 4 are on the right side.
        return [marker_name for marker_name in self.marker_names if marker_name.endswith(("1", "2", "3", "4"))]
    
    def get_left_marker_names(self):
        """
        Returns a list of all left-side marker names from the spider shape definition.
        """
        # The markers with 5, 6, 7, or 8 are on the left side.
        return [marker_name for marker_name in self.marker_names if marker_name.endswith(("5", "6", "7", "8"))]

    def get_frontlegs_marker_names(self):
        """
        Returns a list of all front leg marker names from the spider shape definition.
        """
        return [marker_name for marker_name in self.marker_names if marker_name.endswith(("1", "8"))]

    def get_backlegs_marker_names(self):
        """
        Returns a list of all back leg marker names from the spider shape definition.
        """
        return [marker_name for marker_name in self.marker_names if marker_name.endswith(("4", "5"))]