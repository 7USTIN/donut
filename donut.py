from sys import exit
from math import cos, sin, pi
from signal import signal, SIGINT

size = 55
luminance = ".,-~:;=!*#$@"
theta_spacing = 0.07
phi_spacing = 0.02
a, b = 1, 1
r1, r2 = 1, 2
k2 = 5
k1 = size * k2 * 3 / (8 * (r1 + r2))

def exit_script(*args):
    print("\033[?1049l\033[?25h")
    exit()

def draw(a: float, b: float):
    output = [[" "] * size for i in range(size)]
    zbuffer = [[0] * size for i in range(size)]

    cos_a, sin_a = cos(a), sin(a)
    cos_b, sin_b = cos(b), sin(b)
    theta = 0

    while (theta <= 2 * pi):
        theta += theta_spacing
        cos_theta, sin_theta = cos(theta), sin(theta)
        phi = 0

        while (phi <= 2 * pi):
            phi += phi_spacing
            cos_phi, sin_phi = cos(phi), sin(phi)

            circle_x = r2 + r1 * cos_theta
            circle_y = r1 * sin_theta

            x = circle_x * (cos_b * cos_phi + sin_a * sin_b * sin_phi) - circle_y * cos_a * sin_b
            y = circle_x * (sin_b * cos_phi - sin_a * cos_b * sin_phi) + circle_y * cos_a * cos_b
            z = k2 + cos_a * circle_x * sin_phi + circle_y * sin_a
            ooz = 1 / z
            
            x_p = int(size / 2 + k1 * ooz * x)
            y_p = int(size / 2 - k1 * ooz * y)

            l = cos_phi * cos_theta * sin_b - cos_a * cos_theta * sin_phi - sin_a * sin_theta + cos_b * (cos_a * sin_theta - cos_theta * sin_a * sin_phi)

            if (l > 0 and ooz > zbuffer[x_p][y_p]):
                zbuffer[x_p][y_p] = ooz
                luminance_index = int(l * 8)
                output[x_p][y_p] = luminance[luminance_index]

    output_pretty = [[element for item in sublist for element in (item, item)] for sublist in output]

    print("\033[H\033[J")
    print(*["".join(row) for row in output_pretty], sep="\n")

if __name__ == "__main__":
    print("\033[?1049h\033[?25l")
    signal(SIGINT, exit_script)

    while True:
        a += theta_spacing
        b += phi_spacing
        draw(a, b)
