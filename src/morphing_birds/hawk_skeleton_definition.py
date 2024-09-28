from .SkeletonDefinition import SkeletonDefinition

class HawkSkeletonDefinition(SkeletonDefinition):
    def __init__(self):
        marker_names = [
            "left_wingtip", "right_wingtip", 
            "left_primary", "right_primary", 
            "left_secondary", "right_secondary", 
            "left_tailtip", "right_tailtip"
        ]
        fixed_marker_names = [
            "left_shoulder", "left_tailbase", "right_tailbase", 
            "right_shoulder", "hood", "tailpack"
        ]
        body_sections = {
            "left_handwing": ["left_wingtip", "left_primary", "left_secondary"],
            "right_handwing": ["right_wingtip", "right_primary", "right_secondary"],
            "left_armwing": ["left_primary", "left_secondary", "left_tailbase", "left_shoulder"],
            "right_armwing": ["right_primary", "right_secondary", "right_tailbase", "right_shoulder"],
            "body": ["right_shoulder", "left_shoulder", "left_tailbase", "right_tailbase"],
            "head": ["right_shoulder", "hood", "left_shoulder"],
            "tail": ["right_tailtip", "left_tailtip", "left_tailbase", "right_tailbase"],
        }
        super().__init__(marker_names, fixed_marker_names, body_sections)

    def get_all_marker_names(self):
        return self.marker_names + self.fixed_marker_names