import pygame
import os
pygame.font.init()
pygame.mixer.init()

bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
VEL = 5
red_bullet = []
yellow_bullet = []
bullet_vel = 7
max_bullet = 3
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('comicsans', 100)

YELLOW_SPACESHIP = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

RED_SPACESHIP = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)
space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health):
	WIN.blit(space, (0, 0))
	pygame.draw.rect(WIN, BLACK, BORDER)
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x, red.y))

	red_health_text = health_font.render("Health : " + str(red_health), 1, WHITE)
	yellow_health_text = health_font.render("Health : " + str(yellow_health), 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10 ))
	WIN.blit(yellow_health_text, (10, 10))

	for bullet in yellow_bullet:
		pygame.draw.rect(WIN, YELLOW, bullet)
	for bullet in red_bullet:
		pygame.draw.rect(WIN, RED, bullet)

	pygame.display.update()

def yellow_movement_handle(key_pressed, yellow):
		if key_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
			yellow.x -= VEL
		if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width< BORDER.x: #right
			yellow.x += VEL
		if key_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
			yellow.y -= VEL
		if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 15 < HEIGHT: #down
			yellow.y += VEL

def red_movement_handle(key_pressed, red):
		if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
			red.x -= VEL
		if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
			red.x += VEL
		if key_pressed[pygame.K_UP] and red.y - VEL > 0: #up
			red.y -= VEL
		if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 15< HEIGHT: #down
			red.y += VEL
	
def handle_bullets(yellow_bullet, red_bullet, yellow, red):
	for bullet in yellow_bullet:
		bullet.x += bullet_vel
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(red_hit))
			yellow_bullet.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullet.remove(bullet)

	for bullet in red_bullet:
		bullet.x -= bullet_vel
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(yellow_hit))
			red_bullet.remove(bullet)
		elif bullet.x < 0:
			red_bullet.remove(bullet)

def draw_winner(text):
	draw_text = winner_font.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(5000)


def main():
	red = pygame.Rect(745, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
	yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) 
	red_bullet = []
	yellow_bullet = []
	red_health = 10
	yellow_health = 10

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullet) < max_bullet:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2, 10, 5)
					yellow_bullet.append(bullet)
					bullet_fire_sound.play()

				if event.key == pygame.K_RCTRL and len(red_bullet) < max_bullet:
					bullet = pygame.Rect(red.x, red.y + red.height/2, 10, 5)
					red_bullet.append(bullet)
					bullet_fire_sound.play()
			
			if event.type == red_hit:
				red_health -= 1
				bullet_hit_sound.play()

			if event.type == yellow_hit:
				yellow_health -= 1
				bullet_hit_sound.play()
			
		winner_text = ""

		
		if red_health <= 0:
			winner_text = "Yellow Wins!"

		if yellow_health <= 0:
			winner_text = "Red Wins!"

		if winner_text != "":
			draw_winner(winner_text)
			break

		# print(red_bullet, yellow_bullet)
		key_pressed = pygame.key.get_pressed()
		yellow_movement_handle(key_pressed, yellow)
		red_movement_handle(key_pressed, red)
		handle_bullets(yellow_bullet, red_bullet, yellow, red)

		draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health)
	main()

if __name__ == '__main__':
	main() 