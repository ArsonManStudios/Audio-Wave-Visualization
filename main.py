import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import pygame

pygame.init()
clock = pygame.time.Clock()
run = True
GREEN = [(0, 255, 0),
         (0, 156, 0),
         (0, 71, 0)]
BLACK = (0, 0, 0)

size = (1000, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Audio Wave Visualization')
h = screen.get_height()
w = screen.get_width()

file_path = 'points_of_authority.mp3'
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
            points1 = np.column_stack((points, func1(points, map_value(amp, 0, 0.3, 25, 100),  dtime/150)))
            points2 = np.column_stack((points, func2(points, map_value(amp, 0, 0.3, 25, 150),  dtime/250)))
            points3 = np.column_stack((points, func3(points, map_value(amp, 0, 0.3, 25, 200),  dtime/500)))
            screen.fill(BLACK)
            pygame.draw.lines(screen, GREEN[2], False, points3, 2)
            pygame.draw.lines(screen, GREEN[1], False, points2, 2)
            pygame.draw.lines(screen, GREEN[0], False, points1, 2)
            i += chunk_size
        pygame.display.flip()
        clock.tick(60)
pygame.quit()