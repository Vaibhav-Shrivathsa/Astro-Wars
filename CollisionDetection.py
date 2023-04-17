from pygame.math import Vector2

def clamp(min, val, max):
    if val > max:
        return max
    elif val < min:
        return min
    else:
        return val


class InvertedRectangle:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def contains_point(self, point):
        return not (self.top_left[0] < point[0] < self.bottom_right[0] and
                    self.bottom_right[1] < point[1] < self.top_left[1])

    def closest_point_on_boundary_to(self, point):
        boundary_point = Vector2(clamp(self.top_left[0], point[0], self.bottom_right[0]),
                                 clamp(self.bottom_right[1], point[1], self.top_left[1]))
        if boundary_point == point:
            left_dist = point[0] - self.top_left[0]
            right_dist = self.bottom_right[0] - point[0]
            top_dist = self.top_left[1] - point[1]
            bottom_dist = point[1] - self.bottom_right[1]
            min_dist = min(left_dist, right_dist, top_dist, bottom_dist)

            if min_dist == left_dist:
                boundary_point[0] = self.top_left[0]
            elif min_dist == right_dist:
                boundary_point[0] = self.bottom_right[0]
            elif min_dist == top_dist:
                boundary_point[1] = self.top_left[1]
            else:
                boundary_point[1] = self.bottom_right[1]
        return boundary_point


class Rectangle:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def contains_point(self, point):
        return self.top_left[0] <= point[0] <= self.bottom_right[0] and \
            self.bottom_right[1] <= point[1] <= self.top_left[1]

    def closest_point_on_boundary_to(self, point):
        boundary_point = Vector2(clamp(self.top_left[0], point[0], self.bottom_right[0]),
                                 clamp(self.bottom_right[1], point[1], self.top_left[1]))
        if boundary_point == point:
            left_dist = self.top_left[0] - point[0]
            right_dist = point[0] - self.bottom_right[0]
            top_dist = point[1] - self.top_left[1]
            bottom_dist = self.bottom_right[1] - point[1]
            min_dist = min(left_dist, right_dist, top_dist, bottom_dist)

            if min_dist == left_dist:
                boundary_point[0] = self.top_left[0]
            elif min_dist == right_dist:
                boundary_point[0] = self.bottom_right[0]
            elif min_dist == top_dist:
                boundary_point[1] = self.top_left[1]
            else:
                boundary_point[1] = self.bottom_right[1]
        return boundary_point


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains_point(self, point):
        return (self.center - point).length_squared <= self.radius ** 2

    def is_colliding_with_circle(self, circle):
        return self.center.distance_squared_to(circle.center) <= self.radius ** 2

    def is_colliding_with_rect(self, rect):
        boundary_point = rect.closest_point_on_boundary_to(self.center)
        return self.center.distance_squared_to(boundary_point) < self.radius ** 2 or \
            rect.contains_point(self.center)

    def is_colliding_with_inverted_rect(self, rect):
        boundary_point = rect.closest_point_on_boundary_to(self.center)
        return self.center.distance_squared_to(boundary_point) < self.radius ** 2 or \
            rect.contains_point(self.center)

    def fix_collision_with_circle(self, circle):
        if self.is_colliding_with_circle(circle):
            self.center = (self.center - circle.center).scale_to_length(circle.radius) + \
                          circle.center

    def get_entry_point_into_rect(self, rect, self_vel):
        closest_point_on_boundary = rect.closest_point_on_boundary_to(self.center)
        rect_point_deepest_in_circle = closest_point_on_boundary

        penetration_vector = rect_point_deepest_in_circle - self.center
        if penetration_vector == Vector2(0, 0):
            penetration_vector = (rect.top_left + rect.bottom_right) / 2 - self.center
        penetration_vector.scale_to_length(self.radius)

        circle_point_deepest_in_rect = self.center + penetration_vector
        resolve_displacement = rect_point_deepest_in_circle - circle_point_deepest_in_rect

        new_vel = None
        if closest_point_on_boundary[0] == rect.top_left[0] or closest_point_on_boundary[0] == rect.bottom_right[0]:
            new_vel = Vector2(0, self_vel[1])
        else:
            new_vel = Vector2(self_vel[0], 0)

        return self.center + resolve_displacement, new_vel

    def fix_collision_with_rect(self, rect, self_vel):
        if self.is_colliding_with_rect(rect):
            self.center, new_vel = self.get_entry_point_into_rect(rect, self_vel)
            return self.center, new_vel
        return self.center, self_vel

    def fix_collision_with_inverted_rect(self, rect, self_vel):
        if self.is_colliding_with_inverted_rect(rect):
            self.center, new_vel = self.get_entry_point_into_rect(rect, self_vel)
            return self.center, new_vel
        return self.center, self_vel


def ray_vertical_line_collision(ray_root, ray, v_line_x):
    if ray[0] == 0:
        if ray_root[0] == v_line_x:
            return ray_root
        return None
    else:
        scale_factor = (v_line_x - ray_root[0]) / ray[0]
        return ray * scale_factor + ray_root


def ray_horizontal_line_collision(ray_root, ray, h_line_y):
    if ray[1] == 0:
        if ray_root[1] == h_line_y:
            return ray_root
        return None
    else:
        scale_factor = (h_line_y - ray_root[1]) / ray[1]
        return ray * scale_factor + ray_root
