import pygame
import os
import numpy as np

pygame.font.init()

WIDTH, HEIGHT = 900, 504
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

FPS = 60

WHITE = (255, 255, 255)
SCORE_FONT = pygame.font.Font(os.path.join('Assets', 'flappy bird font.TTF'), 48)

BIRD_SIZE_WIDTH = 51
BIRD_SIZE_HEIGHT = 36
SPAWN_POSITION_X = 100
SPAWN_POSITION_Y = 200
BIRD_ACCELERATION = 0.5
FLAP_VELOCITY = -10

PIPE_SIZE_WIDTH = 70
PIPE_SIZE_HEIGHT = 250
PIPE_SPEED = -3
PIPE_GAP = 400
PIPE_DISTANCE = 300
PIPE_POSITION_MIN = 260
PIPE_POSITION_MAX = 400

BACKGROUND_SPRITE = pygame.image.load(os.path.join('Assets', 'background.png'))

BOTTOM_PIPE_SPRITE = pygame.image.load(os.path.join('Assets', 'bottom pipe.png'))
BOTTOM_PIPE = pygame.transform.scale(BOTTOM_PIPE_SPRITE, (PIPE_SIZE_WIDTH, PIPE_SIZE_HEIGHT))

TOP_PIPE_SPRITE = pygame.image.load(os.path.join('Assets', 'top pipe.png'))
TOP_PIPE = pygame.transform.scale(TOP_PIPE_SPRITE, (PIPE_SIZE_WIDTH, PIPE_SIZE_HEIGHT))

BIRD_SPRITE = pygame.image.load(os.path.join('Assets', 'bird sprite.png'))
BIRD = pygame.transform.scale(BIRD_SPRITE, (BIRD_SIZE_WIDTH, BIRD_SIZE_HEIGHT))

class Bird():
	def __init__(self, rect):
		self.rect = rect
		self.velocity = 0
		self.acceleration = BIRD_ACCELERATION

	def flap(self):
		self.velocity = FLAP_VELOCITY

	def update(self):
		if self.velocity <= 0 and self.acceleration == BIRD_ACCELERATION: 
			self.acceleration *= 1.5
		elif self.acceleration != BIRD_ACCELERATION:
			self.acceleration /= 1.5

		self.velocity += self.acceleration

		self.rect.y += self.velocity

class Pipe():
	def __init__(self, rect, sprite):
		self.rect = rect
		self.sprite = sprite
		self.passed = False

def draw_window(bird, pipes, score):
	WIN.blit(BACKGROUND_SPRITE, (0, 0))

	for pipe in pipes:
		WIN.blit(pipe.sprite, (pipe.rect.x, pipe.rect.y))

	WIN.blit(BIRD, (bird.rect.x, bird.rect.y))

	score_text = SCORE_FONT.render(str(int(score)), 1, WHITE)
	WIN.blit(score_text, (WIDTH / 2, 50))

	pygame.display.update()

def addPipe(pipes):
	yPosition = np.random.randint(PIPE_POSITION_MIN, PIPE_POSITION_MAX)
	newPipeRect = pygame.Rect(WIDTH, yPosition, PIPE_SIZE_WIDTH, PIPE_SIZE_HEIGHT)
	newPipe = Pipe(newPipeRect, BOTTOM_PIPE)
	pipes.append(newPipe)
	newPipeRect = pygame.Rect(WIDTH, yPosition - PIPE_GAP, PIPE_SIZE_WIDTH, PIPE_SIZE_HEIGHT)
	newPipe = Pipe(newPipeRect, TOP_PIPE)
	pipes.append(newPipe)

def checkCollision(bird, pipes):
	for pipe in pipes:
		if bird.rect.colliderect(pipe.rect):
			return True
	return False

def main():
	global birds
	global FPS
	global high_score

	birdRect = pygame.Rect(SPAWN_POSITION_X, SPAWN_POSITION_Y, BIRD_SIZE_WIDTH, BIRD_SIZE_HEIGHT)
	bird = Bird(birdRect)

	pipes = []
	addPipe(pipes)

	spacePressed = False

	score = 0

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		spaceState = pygame.key.get_pressed()[pygame.K_SPACE]
		if spaceState == True and spacePressed == False:
			spacePressed = True
			bird.flap()

		if spaceState == False and spacePressed == True:
			spacePressed = False

		if len(pipes) == 0:
			addPipe(pipes)

		if pipes[-1].rect.x < WIDTH - PIPE_DISTANCE:
			addPipe(pipes)

		if pipes[0].rect.x < -60:
			pipes.pop(0)
			pipes.pop(0)

		for pipe in pipes:
			pipe.rect.x += PIPE_SPEED

			if pipe.rect.x + PIPE_SIZE_WIDTH < SPAWN_POSITION_X and pipe.passed == False:
				pipe.passed = True
				score += 0.5

		bird.update()

		if bird.rect.y > WIDTH - 400 or bird.rect.y < -50 or checkCollision(bird, pipes):
			run = False

		draw_window(bird, pipes, score)

	main()

if __name__ == "__main__":
	main()