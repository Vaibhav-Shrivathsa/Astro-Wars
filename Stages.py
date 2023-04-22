from pygame import Vector2
import CollisionDetection


class IndestructableBlock:
    COLOR = (17, 87, 250)
    THICKNESS = 0.05

    def __init__(self, center, size):
        self.center = center
        self.size = size
        reflected_size = Vector2(size[0], -size[1])
        self.collider = \
            CollisionDetection.Rectangle(center - reflected_size / 2
                                         , center + reflected_size / 2)


class DestructableBlock:
    COLOR = (252, 205, 104)
    THICKNESS = 0.05

    def __init__(self, center, size):
        self.center = center
        self.size = size
        reflected_size = Vector2(size[0], -size[1])
        self.collider = \
            CollisionDetection.Rectangle(center - reflected_size / 2
                                         , center + reflected_size / 2)


class OuterBoundary:
    COLOR = (17, 87, 250)
    THICKNESS = .1

    def __init__(self, center, size):
        self.center = center
        self.size = size
        reflected_size = Vector2(size[0], -size[1])
        self.collider = \
            CollisionDetection.InvertedRectangle(center - reflected_size / 2
                                                 , center + reflected_size / 2)


class Stage:
    """
    Class Representing A Level For the Game and Its Associated Objects
    """
    def __init__(self, destructable_blocks, indestructable_blocks,
                 outer_boundary):
        self.destructable_blocks = destructable_blocks
        self.indestructable_blocks = indestructable_blocks
        self.outer_boundary = outer_boundary


class PlayableStages:
    """
    The Stages That Can Be Loaded Up For A Match
    """
    BASIC = None


# Constructing the Playable Stages

basic_destructable_blocks = \
    {DestructableBlock(Vector2(6.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(5.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(4.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(3.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(-6.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(-5.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(-4.5, 0), Vector2(1, 1)),
     DestructableBlock(Vector2(-3.5, 0), Vector2(1, 1))}
basic_indestructable_blocks = \
    {IndestructableBlock(Vector2(0, 0), Vector2(6, 1)),
     IndestructableBlock(Vector2(0, 0), Vector2(1, 6)),
     IndestructableBlock(Vector2(8.5, 0), Vector2(3, 1)),
     IndestructableBlock(Vector2(-8.5, 0), Vector2(3, 1))}
basic_outer_boundary = OuterBoundary(Vector2(0, 0), Vector2(20, 20))
PlayableStages.BASIC = Stage(basic_destructable_blocks,
                             basic_indestructable_blocks, basic_outer_boundary)
