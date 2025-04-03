import numpy as np
import pygame


class Camera:
    def __init__(self, position=(0.0, 0.0, -5.0), pitch=0.0, yaw=0.0, roll=0.0):
        self.position = np.array(position)
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def move(self, dx, dy, dz):
        move_speed_scale = 0.25
        self.position += np.array([dx * move_speed_scale, dy * move_speed_scale, dz * move_speed_scale])

    def rotate(self, dpitch, dyaw, droll):
        rotation_speed_scale = 0.5
        self.pitch += dpitch * rotation_speed_scale
        self.yaw += dyaw * rotation_speed_scale
        self.roll += droll * rotation_speed_scale


def project_to_2d(point, width, height, focal_length=1):
    x, y, z = point
    if z == 0:
        z = 0.0001

    z_scale = 0.25
    z = z * z_scale

    if z <= 0.0:
        z = 0.0001

    projected_x = focal_length * x / z
    projected_y = focal_length * y / z

    return np.array([projected_x, projected_y])


def draw_cube(camera, screen, width, height):
    ver1 = np.array([
        [-1.0, -1.0, 1.0],
        [1.0, -1.0, 1.0],
        [1.0, 1.0, 1.0],
        [-1.0, 1.0, 1.0],
        [-1.0, -1.0, -1.0],
        [1.0, -1.0, -1.0],
        [1.0, 1.0, -1.0],
        [-1.0, 1.0, -1.0]
    ])

    ver2 = np.array([
        [2.0, -1.0, 2.0],
        [4.0, -1.0, 2.0],
        [4.0, 3.0, 2.0],
        [2.0, 3.0, 2.0],
        [2.0, -1.0, -1.0],
        [4.0, -1.0, -1.0],
        [4.0, 3.0, -1.0],
        [2.0, 3.0, -1.0]
    ])

    ver3 = np.array([
        [1.0, 0.0, 6.0],
        [3.0, 0.0, 6.0],
        [2.5, 3.0, 5.5],
        [1.5, 3.0, 5.5],
        [1.0, 0.0, 4.0],
        [3.0, 0.0, 4.0],
        [2.5, 3.0, 4.5],
        [1.5, 3.0, 4.5]
    ])

    edges = [
        [0, 1],
        [0, 3],
        [0, 4],
        [1, 2],
        [1, 5],
        [2, 3],
        [2, 6],
        [3, 7],
        [4, 5],
        [4, 7],
        [5, 6],
        [6, 7]
    ]

    ver_all = [ver1, ver2, ver3]

    for vertices in ver_all:
        vertices -= camera.position

        cos_yaw = np.cos(np.radians(camera.yaw))
        sin_yaw = np.sin(np.radians(camera.yaw))
        cos_pitch = np.cos(np.radians(camera.pitch))
        sin_pitch = np.sin(np.radians(camera.pitch))
        cos_roll = np.cos(np.radians(camera.roll))
        sin_roll = np.sin(np.radians(camera.roll))

        rotation_yaw = np.array([
            [cos_yaw, 0, sin_yaw],
            [0, 1, 0],
            [-sin_yaw, 0, cos_yaw]
        ])

        rotation_pitch = np.array([
            [1, 0, 0],
            [0, cos_pitch, -sin_pitch],
            [0, sin_pitch, cos_pitch]
        ])

        rotation_roll = np.array([
            [cos_roll, -sin_roll, 0],
            [sin_roll, cos_roll, 0],
            [0, 0, 1]
        ])

        rotation_matrix = np.dot(rotation_roll, np.dot(rotation_pitch, rotation_yaw))

        vertices = np.dot(vertices, rotation_matrix.T)

        for edge in edges:
            start = project_to_2d(vertices[edge[0]], width, height)
            end = project_to_2d(vertices[edge[1]], width, height)

            start_z = vertices[edge[0]][2]
            end_z = vertices[edge[1]][2]

            if start_z < 0.0 and end_z < 0.0:
                continue

            pygame.draw.line(screen, (255, 255, 255),
                             (width / 2 + start[0] * 100, height / 2 - start[1] * 100),
                             (width / 2 + end[0] * 100, height / 2 - end[1] * 100), 1)


def handle_keyboard_input(camera):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera.move(0.0, 0.0, 1.0)
    if keys[pygame.K_s]:
        camera.move(0.0, 0.0, -1.0)
    if keys[pygame.K_a]:
        camera.move(-1.0, 0.0, 0.0)
    if keys[pygame.K_d]:
        camera.move(1.0, 0.0, 0.0)
    if keys[pygame.K_SPACE]:
        camera.move(0.0, 1.0, 0.0)
    if keys[pygame.K_LSHIFT]:
        camera.move(0.0, -1.0, 0.0)

    if keys[pygame.K_UP]:
        camera.rotate(1.0, 0.0, 0.0)
    if keys[pygame.K_DOWN]:
        camera.rotate(-1.0, 0.0, 0.0)
    if keys[pygame.K_RIGHT]:
        camera.rotate(0.0, -1.0, 0.0)
    if keys[pygame.K_LEFT]:
        camera.rotate(0.0, 1.0, 0.0)
    if keys[pygame.K_e]:
        camera.rotate(0.0, 0.0, 1.0)
    if keys[pygame.K_q]:
        camera.rotate(0.0, 0.0, -1.0)


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Virtual camera")

camera = Camera()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keyboard_input(camera)
    screen.fill((0, 0, 0))
    draw_cube(camera, screen, width, height)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
