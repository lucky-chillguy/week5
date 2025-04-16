import pygame
import random
import os

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 480, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1945 Strike")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 이미지 로드
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.cool_down = 0
        self.cool_down_time = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        
        # 쿨다운 업데이트
        if self.cool_down > 0:
            self.cool_down -= 1
            
    def shoot(self):
        if self.cool_down <= 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.cool_down = self.cool_down_time

# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # 화면 밖으로 나가면 삭제
        if self.rect.bottom < 0:
            self.kill()

# 폭발 클래스
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= 3:
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.Surface((30, 30))
                self.image.fill((255, 255 - self.frame * 50, 0))
                self.rect = self.image.get_rect()
                self.rect.center = center

# 게임 점수 표시
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# 게임 스프라이트 그룹
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# 적 생성
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 게임 속성
score = 0
running = True
clock = pygame.time.Clock()

# 게임 루프
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 업데이트
    all_sprites.update()

    # 자동 발사 (스페이스바를 누르지 않아도)
    player.shoot()

    # 충돌 체크 (총알과 적)
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 충돌 체크 (플레이어와 적)
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f"점수: {score}", 30, WIDTH // 2, 10)
    
    # 화면 갱신
    pygame.display.flip()
    
    # FPS 설정
    clock.tick(60)

pygame.quit() 