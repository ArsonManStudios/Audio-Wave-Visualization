import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import pygame

pygame.init()
clock = pygame.time.Clock()
run = True
RED   = [(255, 0, 0),
         (156, 0, 0),
         (71, 0, 0)]
GREEN = [(0, 255, 0),
         (0, 156, 0),
         (0, 71, 0)]
BLUE  = [(0, 0, 255),
         (0, 0, 156),
         (0, 0, 71)]
BLACK = (0, 0, 0)

# 0: Red
# 1: Green
# 2: Blue
rgb_choice = [1, 1, 1]
seperation = 0.25

points_red1 = [(-10, -10), (-10, -10)]
points_red2 = [(-10, -10), (-10, -10)]
points_red3 = [(-10, -10), (-10, -10)]
points_green1 = [(-10, -10), (-10, -10)]
points_green2 = [(-10, -10), (-10, -10)]
points_green3 = [(-10, -10), (-10, -10)]
points_blue1 = [(-10, -10), (-10, -10)]
points_blue2 = [(-10, -10), (-10, -10)]
points_blue3 = [(-10, -10), (-10, -10)]

size = (1000, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Audio Wave Visualization')
h = screen.get_height()
w = screen.get_width()

file_path = 'cure_for_teh_itch.mp3'
chunk_size = 2048
point_freq = w

audio, sample_rate = sf.read(file_path, dtype='float32')

# Stereo to mono
if audio.ndim > 1:
    audio = audio.mean(axis=1)

def info(chunk):
    # Amplitude calculated from root mean square
    amplitude = np.sqrt(np.mean(chunk**2))
    return amplitude

def map_value(value, input_min, input_max, output_min, output_max):
    proportion = float(value-input_min)/float(input_max-input_min)
    mapped_value = output_min+proportion*(output_max-output_min)
    return mapped_value

def func1(x, amp, offset):
    return amp*np.sin(0.03*x+offset) + h/2
def func2(x, amp, offset):
    return amp*np.sin(0.03*x+offset) + amp*np.sin(0.05*x+offset) + h/2
def func3(x, amp, offset):
    return amp*np.sin(0.03*x+offset) + amp*np.sin(0.05*x+offset) + amp*np.sin(0.07*x+offset) + h/2

# Play audio
i = 0
with sd.OutputStream(
    samplerate=sample_rate,
    channels=1,
    blocksize=chunk_size
) as stream:
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill(BLACK)
        if i <= len(audio):
            chunk = audio[i:i + chunk_size]
            if len(chunk) < chunk_size:
                break
            stream.write(chunk.reshape(-1, 1))
            amp = info(chunk)
            dtime = pygame.time.get_ticks()
            points = np.linspace(0, w, point_freq)
            if rgb_choice[0]:
                points_red1 = np.column_stack((points, func1(points, map_value(amp, 0, 0.3, 0, 100),  dtime/150+seperation)))
                points_red2 = np.column_stack((points, func2(points, map_value(amp, 0, 0.3, 0, 150),  dtime/250+seperation)))
                points_red3 = np.column_stack((points, func3(points, map_value(amp, 0, 0.3, 0, 200),  dtime/500+seperation)))
            if rgb_choice[1]:
                points_green1 = np.column_stack((points, func1(points, map_value(amp, 0, 0.3, 0, 100),  dtime/150)))
                points_green2 = np.column_stack((points, func2(points, map_value(amp, 0, 0.3, 0, 150),  dtime/250)))
                points_green3 = np.column_stack((points, func3(points, map_value(amp, 0, 0.3, 0, 200),  dtime/500)))
            if rgb_choice[2]:
                points_blue1 = np.column_stack((points, func1(points, map_value(amp, 0, 0.3, 0, 100),  dtime/150-seperation)))
                points_blue2 = np.column_stack((points, func2(points, map_value(amp, 0, 0.3, 0, 150),  dtime/250-seperation)))
                points_blue3 = np.column_stack((points, func3(points, map_value(amp, 0, 0.3, 0, 200),  dtime/500-seperation)))
            screen.fill(BLACK)
            pygame.draw.lines(screen, RED[2], False, points_red3, 2)
            pygame.draw.lines(screen, GREEN[2], False, points_green3, 2)
            pygame.draw.lines(screen, BLUE[2], False, points_blue3, 2)
            pygame.draw.lines(screen, RED[1], False, points_red2, 2)
            pygame.draw.lines(screen, GREEN[1], False, points_green2, 2)
            pygame.draw.lines(screen, BLUE[1], False, points_blue2, 2)
            pygame.draw.lines(screen, RED[0], False, points_red1, 2)
            pygame.draw.lines(screen, GREEN[0], False, points_green1, 2)
            pygame.draw.lines(screen, BLUE[0], False, points_blue1, 2)
            i += chunk_size
        pygame.display.flip()
        clock.tick(60)
pygame.quit()