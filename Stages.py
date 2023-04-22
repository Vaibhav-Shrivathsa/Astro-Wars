from pygame import Vector2
import CollisionDetection


class IndestructableBlock:
    COLOR = (17, 87, 250)
    THICKNESS = 0.05

    def __init__(self, center, size):
        self.center = center
        self.size = size
        reflected_size = Vector2(size[0], -size[1])
        self.collider = CollisionDetection.Rectangle(center - reflected_size / 2,
                                                     center + reflected_size / 2)


class DestructableBlock:
    COLOR = (252, 205, 104)
    THICKNESS = 0.05

    def __init__(self, center, size):
        self.center = center
        self.size = size
        reflected_size = Vector2(size[0], -size[1])
        self.collider = CollisionDetection.Rectangle(center - reflected_size / 2,
                                                     center + reflected_size / 2)


class OuterBoundary:
    COLOR = (17, 87, 250)
    THICKNESS = .1

    def __init__(self, center, size):
        self.center = center
        self.size = size
        reflected_size = Vector2(size[0], -size[1])
        self.collider = CollisionDetection.InvertedRectangle(center - reflected_size / 2,
                                                             center + reflected_size / 2)


class Stage:
    """
    Class Representing A Level For the Game and Its Associated Objects
    """

    def __init__(self, destructable_blocks, indestructable_blocks, outer_boundary):
        self.destructable_blocks = destructable_blocks
        self.indestructable_blocks = indestructable_blocks
        self.outer_boundary = outer_boundary


class PlayableStages:
    """
    The Stages That Can Be Loaded Up For A Match
    """
    STAGELIST = []


# Constructing the Playable Stages

# STAGE 1: Plus in Center
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
PlayableStages.STAGELIST.append(Stage(basic_destructable_blocks,
                                      basic_indestructable_blocks, basic_outer_boundary))


def make_horiz_line_of_blocks(start_x, end_x, y):
    line = set()
    for x in range(int(end_x - start_x + 1)):
        line.add(DestructableBlock(Vector2(start_x + x, y),
                                   Vector2(1, 1)))
    return line


def make_vert_line_of_blocks(start_y, end_y, x):
    line = set()
    for y in range(int(end_y - start_y + 1)):
        line.add(DestructableBlock(Vector2(x, start_y + y),
                                   Vector2(1, 1)))
    return line

# STAGE 2: All Destructable
basic_destructable_blocks = set()
basic_destructable_blocks |= make_horiz_line_of_blocks(6.5, 9.5, 6.5)
basic_destructable_blocks |= make_vert_line_of_blocks(6.5, 9.5, 6.5)
basic_destructable_blocks |= make_horiz_line_of_blocks(-9.5, -6.5, 6.5)
basic_destructable_blocks |= make_vert_line_of_blocks(6.5, 9.5, -6.5)
basic_destructable_blocks |= make_horiz_line_of_blocks(-9.5, -6.5, -6.5)
basic_destructable_blocks |= make_vert_line_of_blocks(-9.5, -6.5, -6.5)
basic_destructable_blocks |= make_horiz_line_of_blocks(6.5, 9.5, -6.5)
basic_destructable_blocks |= make_vert_line_of_blocks(-9.5, -6.5, 6.5)

basic_destructable_blocks |= make_horiz_line_of_blocks(-9.5, -1.5, 0.5)
basic_destructable_blocks |= make_horiz_line_of_blocks(1.5, 9.5, 0.5)
basic_destructable_blocks |= make_horiz_line_of_blocks(-9.5, -1.5, -0.5)
basic_destructable_blocks |= make_horiz_line_of_blocks(1.5, 9.5, -0.5)

basic_destructable_blocks |= make_vert_line_of_blocks(-9.5, -1.5, 0.5)
basic_destructable_blocks |= make_vert_line_of_blocks(1.5, 9.5, 0.5)
basic_destructable_blocks |= make_vert_line_of_blocks(-9.5, -1.5, -0.5)
basic_destructable_blocks |= make_vert_line_of_blocks(1.5, 9.5, -0.5)

basic_destructable_blocks |= make_vert_line_of_blocks(-0.5, 0.5, -0.5)
basic_destructable_blocks |= make_vert_line_of_blocks(-0.5, 0.5, 0.5)

basic_indestructable_blocks = set()
basic_outer_boundary = OuterBoundary(Vector2(0, 0), Vector2(20, 20))
PlayableStages.STAGELIST.append(Stage(basic_destructable_blocks,
                                      basic_indestructable_blocks, basic_outer_boundary))

# Stage 3: Square in Center
basic_destructable_blocks = set()
basic_indestructable_blocks = {IndestructableBlock(Vector2(0, 0), Vector2(5, 5))}
basic_outer_boundary = OuterBoundary(Vector2(0, 0), Vector2(20, 20))
PlayableStages.STAGELIST.append(Stage(basic_destructable_blocks,
                                      basic_indestructable_blocks, basic_outer_boundary))