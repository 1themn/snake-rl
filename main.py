import pygame, sys, random
from pygame.math import Vector2
from pathfinding import bfs, astar
import time

class SNAKE:
    def __init__(self, start_pos, direction):
        self.direction = Vector2(direction)
        self.body = [
            Vector2(start_pos) - i * self.direction
            for i in range(3)
        ]
        self.new_block = False
        self.score = 0
        self.nodes_explored = 0
        self.search_time = 0
        self.path_length = 0
        self.total_nodes_explored = 0
        self.total_search_time = 0
        self.search_count = 0
        

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame. image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)    
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)


            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y ==-1 or previous_block.y ==-1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y ==1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y ==-1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y ==1 or previous_block.y ==1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                     

            # else:
            #     pygame.draw.rect(screen,(150,100,100),block_rect)
        # for block in self.body:
        #     x_pos = int(block.x*cell_size)
        #     y_pos = int(block.y*cell_size)
        #     block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
        #     pygame.draw.rect(screen,(21, 0, 208),block_rect) 

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down
    
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down 

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self, snakes):
        self.randomize(snakes)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        # pygame.draw.rect(screen,(255, 39, 39),fruit_rect)
    
    # def randomize(self):
    #     self.x = random.randint(0,cell_number-1)
    #     self.y = random.randint(0,cell_number-1)
    #     self.pos = Vector2(self.x,self.y)

    def randomize(self, snakes):
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)

            position = Vector2(x, y)

            occupied = any(
                position in snake.body
                for snake in snakes
            )

            if not occupied:
                self.pos = position
                break

class MAIN:
    def __init__(self):
        self.paused = False
        self.game_ended = False
        self.winner = None      
        self.algorithm1 = "BFS"
        self.algorithm2 = "A*"
        self.snake = SNAKE(
            start_pos=(5, 10),
            direction=(1, 0)
        )
        self.snake2 = SNAKE(
            start_pos=(15, 7),
            direction=(-1, 0)
        )
        self.fruit = FRUIT([self.snake, self.snake2])

    def update(self):
        if self.game_ended:
            return

        previous_head1 = self.snake.body[0].copy()
        previous_head2 = self.snake2.body[0].copy()


        self.move_ai(self.snake, self.algorithm1)
        self.move_ai(self.snake2, self.algorithm2)


        self.snake.move_snake()
        self.snake2.move_snake()

        head1 = self.snake.body[0]
        head2 = self.snake2.body[0]


        snake1_lost = (
            self.check_fail(self.snake)
            or self.check_opponent_collision(self.snake, self.snake2)
        )

        snake2_lost = (
            self.check_fail(self.snake2)
            or self.check_opponent_collision(self.snake2, self.snake)
        )


        head_collision = head1 == head2

        head_swap = (
            head1 == previous_head2
            and head2 == previous_head1
        )

        if head_collision or head_swap:
            snake1_lost = True
            snake2_lost = True


        if snake1_lost and snake2_lost:
            self.game_over("DRAW")
        elif snake1_lost:
            self.game_over("SNAKE 2")
        elif snake2_lost:
            self.game_over("SNAKE 1")
        else:

            self.check_collision(self.snake)
            self.check_collision(self.snake2)

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.snake2.draw_snake()
        self.draw_dashboard()
        if self.game_ended:
            self.draw_game_over()

    def check_collision(self, snake):
        if self.fruit.pos == snake.body[0]:
            snake.score += 1
            snake.add_block()
            self.fruit.randomize([self.snake, self.snake2])


    def check_opponent_collision(self, snake, opponent):
        head = snake.body[0]

        return head in opponent.body


    def check_fail(self, snake):
        head = snake.body[0]

        if not (0 <= head.x < cell_number and 0 <= head.y < cell_number):
            return True

        if head in snake.body[1:]:
            return True

        return False
    
    def move_ai(self, snake, algorithm):
        start = (int(snake.body[0].x), int(snake.body[0].y))
        goal = (int(self.fruit.pos.x), int(self.fruit.pos.y))

        blocked = set()

        for s in [self.snake, self.snake2]:
            for block in s.body:
                blocked.add((int(block.x), int(block.y)))
        neck = snake.body[1]
        blocked.add((int(neck.x), int(neck.y)))
        blocked.discard(start)
        start_time = time.perf_counter()

        if algorithm == "BFS":
            path, nodes = bfs(start, goal, blocked, cell_number)
        elif algorithm == "A*":
            path, nodes = astar(start, goal, blocked, cell_number)
        else:
            return
        
        search_time = (time.perf_counter() - start_time) * 1000
        snake.nodes_explored = nodes
        snake.search_time = search_time
        snake.path_length = len(path)

        snake.total_nodes_explored += nodes
        snake.total_search_time += search_time
        snake.search_count += 1

        if path:
            next_x, next_y = path[0]

            snake.direction = Vector2(
                next_x - start[0],
                next_y - start[1]
            )
        else:
            self.safe_move(snake, blocked)


    def safe_move(self, snake, blocked):
        head = snake.body[0]

        directions = [
            Vector2(0, -1),
            Vector2(0, 1),
            Vector2(-1, 0),
            Vector2(1, 0)
        ]

        for direction in directions:
            new_pos = head + direction
            position = (int(new_pos.x), int(new_pos.y))

            if (
                0 <= new_pos.x < cell_number
                and 0 <= new_pos.y < cell_number
                and position not in blocked
                and direction != -snake.direction
            ):
                snake.direction = direction
                return
            
    def draw_dashboard(self):
        x = board_width + 20

        pygame.draw.rect(
            screen,
            (30, 35, 45),
            (board_width, 0, dashboard_width, board_height)
        )

        font = pygame.font.SysFont("Arial", 24, bold=True)
        small_font = pygame.font.SysFont("Arial", 19)

        title = font.render("AI BATTLE", True, (255, 255, 255))
        screen.blit(title, (x, 25))

        if self.game_ended:
            status = f"Winner: {self.winner}"
        elif self.paused:
            status = "Status: Paused"
        else:
            status = "Status: Running"

        status_text = small_font.render(
            status,
            True,
            (255, 215, 100)
        )

        screen.blit(status_text, (x, 65))

        snakes = [
            (self.snake, self.algorithm1, "SNAKE 1", (80, 220, 130)),
            (self.snake2, self.algorithm2, "SNAKE 2", (90, 150, 255))
        ]

        for i, (snake, algorithm, name, color) in enumerate(snakes):
            y = 100 + i * 300

            heading = font.render(
                f"{name} - {algorithm}", True, color
            )
            screen.blit(heading, (x, y))

            avg_time = (
                snake.total_search_time / snake.search_count
                if snake.search_count > 0 else 0
            )

            avg_nodes = (
                snake.total_nodes_explored / snake.search_count
                if snake.search_count > 0 else 0
            )

            stats = [
                f"Score: {snake.score}",
                f"Nodes explored: {snake.nodes_explored}",
                f"Search time: {snake.search_time:.3f} ms",
                f"Path length: {snake.path_length}",
                f"Avg. nodes: {avg_nodes:.1f}",
                f"Avg. time: {avg_time:.3f} ms"
            ]

            for j, stat in enumerate(stats):
                text = small_font.render(
                    stat, True, (220, 220, 220)
                )
                screen.blit(text, (x, y + 45 + j * 30))
        
    def draw_game_over(self):
        overlay = pygame.Surface((board_width, board_height))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        text_font = pygame.font.SysFont("Arial", 26)

        if self.winner == "DRAW":
            message = "MATCH DRAW!"
        else:
            message = f"{self.winner} WINS!"

        title = title_font.render(message, True, (255, 255, 255))

        score = text_font.render(
            f"BFS: {self.snake.score}  |  A*: {self.snake2.score}",
            True,
            (220, 220, 220)
        )

        restart = text_font.render(
            "Press R to Restart",
            True,
            (180, 220, 180)
        )

        center_x = board_width // 2
        center_y = board_height // 2

        screen.blit(
            title,
            title.get_rect(center=(center_x, center_y - 65))
        )

        screen.blit(
            score,
            score.get_rect(center=(center_x, center_y))
        )

        screen.blit(
            restart,
            restart.get_rect(center=(center_x, center_y + 65))
        )
    def game_over(self, winner):
        self.game_ended = True
        self.winner = winner


cell_size = 40
cell_number = 22
pygame.init()
board_width = cell_number * cell_size
board_height = cell_number * cell_size
dashboard_width = 300

screen = pygame.display.set_mode(
    (board_width + dashboard_width, board_height)
)

pygame.display.set_caption("Snake AI Battle - BFS vs A*")
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()

main_game = MAIN()


SCREEN_UPDATE = pygame.USEREVENT

pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            if not main_game.paused and not main_game.game_ended:
                main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main_game.paused = not main_game.paused
            if event.key == pygame.K_r:
                main_game = MAIN()
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y !=1:
                    main_game.snake.direction = Vector2(0,-1) 
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y !=-1:
                    main_game.snake.direction = Vector2(0,1) 
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = Vector2(1,0) 
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction = Vector2(-1,0) 
            if event.key == pygame.K_w:
                if main_game.snake2.direction.y !=1:
                    main_game.snake2.direction = Vector2(0,-1) 
            if event.key == pygame.K_s:
                if main_game.snake2.direction.y !=-1:
                    main_game.snake2.direction = Vector2(0,1) 
            if event.key == pygame.K_d:
                if main_game.snake2.direction.x !=-1:
                    main_game.snake2.direction = Vector2(1,0) 
            if event.key == pygame.K_a:
                if main_game.snake2.direction.x !=1:
                    main_game.snake2.direction = Vector2(-1,0) 

    screen.fill((191, 221, 103))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
