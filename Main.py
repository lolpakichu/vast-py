import arcade
import random
import os

SCREEN_WIDTH = 826.6666646
SCREEN_HEIGHT = 620
BULLET_SCALE = 3.5
ENEMY_SCALE = 3.5
PLAYER_SCALE = .4
VIEWPORT_MARGIN = 400
RIGHT_MARGIN = 150
BIGBULLET_SCALE = 7


class Class(arcade.Window):
    """ Main application class """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Vast")

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.POWERED_UP = False
        self.BOSS_SPAWNED = False
        self.GAME_OVER = False
        self.WIN = False
        self.BOSS_HEALTH = 5
        self.death_sound = arcade.load_sound("images/deathsound.wav")
        self.hit_sound = arcade.load_sound("images/sound.wav")
        self.sound_track = arcade.load_sound("images/PixelSong.mp3")
        self.view_left = 0
        self.view_bottom = 0
        self.end = False
        arcade.set_background_color(arcade.color.GRAY)

        # --- Keep track of a frame count.
        # --- This is important for doing things every x frames
        self.score = 0
        self.frame_count = 0
        self.frame_count2 = 0

        self.all_sprites_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.enemybullet_list = arcade.SpriteList()

        self.player = arcade.Sprite("images/player2.png", PLAYER_SCALE)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 100
        self.all_sprites_list.append(self.player)

        enemy = arcade.Sprite("images/enemy.png", ENEMY_SCALE)
        enemy.center_x = SCREEN_WIDTH/2
        enemy.center_y = SCREEN_HEIGHT - 100
        enemy.angle = 0
        self.all_sprites_list.append(enemy)
        self.enemy_list.append(enemy)

    def setup(self):
        self.score = 0
        self.frame_count = 0
        self.frame_count2 = 0
        self.POWERED_UP = False
        self.WIN = False
        self.end = False
        self.BOSS_SPAWNED = False

        self.all_sprites_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemybullet_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()

        self.player = arcade.Sprite("images/player2.png", PLAYER_SCALE)
        self.all_sprites_list.append(self.player)
        self.player.center_x = SCREEN_WIDTH/2
        self.player.center_y = SCREEN_HEIGHT - 500

        enemy = arcade.Sprite("images/enemy.png", ENEMY_SCALE)
        enemy.center_x = SCREEN_WIDTH / 2
        enemy.center_y = SCREEN_HEIGHT - 100
        enemy.angle = 0
        self.all_sprites_list.append(enemy)
        self.enemy_list.append(enemy)

    def on_draw(self):
        """Render the screen. """

        arcade.start_render()

        if self.GAME_OVER:
            arcade.set_background_color(arcade.color.BLACK)

            arcade.draw_text(f"Game Over! Your Score Was {self.score} Press Space to Restart", SCREEN_WIDTH/2 - 200,
                                             self.player.center_y, arcade.color.WHITE, 14)
        if self.WIN:
            self.GAME_OVER = False

            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text(f"You won! Your score was:{self.score}  Press Space to Play Again ", 100, self.player.center_y + 300, arcade.color.WHITE, 20)

        if not self.end:
            if self.BOSS_SPAWNED:
                arcade.draw_text(f"Boss Health: {self.BOSS_HEALTH}", SCREEN_WIDTH / 2, self.player.center_y + 350,
                                 arcade.color.WHITE)
            arcade.SpriteList.draw(self.all_sprites_list)
            output = f"Score:{self.score}"
            arcade.draw_text(output, 10, self.view_bottom + 20, arcade.color.WHITE, 14)
            arcade.set_background_color(arcade.color.GRAY)

    def update(self, delta_time):
        """All the logic to move, and the game logic goes here. """
        if self.player.center_x > SCREEN_WIDTH:
            self.player.center_x = SCREEN_WIDTH - 20
        if self.player.center_x < 0:
            self.player.center_x = 20
        if self.WIN:
            self.GAME_OVER = False

        if not self.end:
            for boss in self.boss_list:
                if self.player.center_y > boss.center_y:
                    self.GAME_OVER = True
            if self.frame_count == 600:
                self.BOSS_SPAWNED = True
            hit_list = arcade.check_for_collision_with_list(self.player,
                                                              self.powerup_list)
            if len(hit_list) > 0:
                self.POWERED_UP = True
            for powerup in hit_list:
                    powerup.kill()

            self.enemy_list.update()
            self.bullet_list.update()
            self.enemybullet_list.update()
            self.boss_list.update()

            # --- Add one to the frame count
            self.player.center_y += .3
            self.frame_count2 += 1



            self.frame_count += 1
            '''if self.POWERED_UP:

                print(self.frame_count2)'''

            # Loop through each bullet
            for bullet in self.bullet_list:

                # Check this bullet to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(bullet,
                                                                self.boss_list)

                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.kill()

                # For every coin we hit, add to the score and remove the coin
                for boss in hit_list:
                    self.BOSS_HEALTH -= 1
                    if self.BOSS_HEALTH == 0:
                        print("WINNER")
                        boss.kill()
                        self.score += 100
                        self.WIN = True
                        self.end = True
                    arcade.play_sound(self.hit_sound)


            for bullet in self.bullet_list:

                # Check this bullet to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(bullet,
                                                                self.enemy_list)

                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.kill()

                # For every coin we hit, add to the score and remove the coin
                for enemy in hit_list:
                    enemy.kill()
                    self.score += 10
                    arcade.play_sound(self.hit_sound)

            for enemybullet in self.enemybullet_list:
                hit_list = arcade.check_for_collision_with_list(self.player,
                                                                self.enemybullet_list)
                if len(hit_list) > 0:
                    enemybullet.kill()
                for self.player in hit_list:
                    self.player.kill()
                    self.GAME_OVER = True
                    self.end = True
                    arcade.play_sound(self.death_sound)

                # If the bullet flies off-screen, remove it.
                if enemybullet.bottom > 1200:
                    enemybullet.kill()

                # If the bullet flies off-screen, remove it.
                if enemybullet.bottom < 0:
                    enemybullet.kill()


            for boss in self.boss_list:

            # --- Use the modulus to trigger doing something every 120 frames
                if self.frame_count % 100 == 0:
                    enemybullet = arcade.Sprite("images/bullet.png", BULLET_SCALE)
                    enemybullet.center_x = boss.center_x
                    enemybullet.angle = 0
                    enemybullet.top = boss.bottom
                    enemybullet.change_y = -2
                    self.enemybullet_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)

            for enemy in self.enemy_list:
                if enemy.bottom > 1200:
                    enemy.kill()

                # --- Use the modulus to trigger doing something every 120 frames
                if self.frame_count % 70 == 0:
                    enemybullet = arcade.Sprite("images/bullet.png", BULLET_SCALE)
                    enemybullet.center_x = enemy.center_x
                    enemybullet.angle = 0
                    enemybullet.top = enemy.bottom
                    enemybullet.change_y = -2
                    self.enemybullet_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)
            # --- Use the modulus to trigger doing something every 120 frames
            if self.frame_count % 130 == 0:
                enemy = arcade.Sprite("images/enemy.png", ENEMY_SCALE)
                enemy.center_x = random.randrange(400)
                enemy.center_y = self.player.center_y + 400
                enemy.angle = 0
                self.enemy_list.append(enemy)
                self.all_sprites_list.append(enemy)

            if self.frame_count % 600 == 0:
                boss = arcade.Sprite("images/Boss.png", ENEMY_SCALE)
                boss.center_x = random.randrange(400)
                boss.center_y = self.player.center_y + 400
                boss.angle = 0
                self.boss_list.append(boss)
                self.all_sprites_list.append(boss)

            # Get rid of the bullet when it flies off-screen
            for bullet in self.bullet_list:
                if bullet.top < -10000:
                    bullet.kill()
            for boss in self.boss_list:
                if self.frame_count % 120 == 0:
                    enemybullet = arcade.Sprite("images/bullet.png", 3.5)
                    enemybullet.center_x = boss.center_x
                    enemybullet.angle = 0
                    enemybullet.top = boss.bottom
                    enemybullet.change_y = -2
                    self.enemybullet_list.append(enemybullet)
                    self.all_sprites_list.append(enemybullet)
                if self.frame_count % 120 == 0:
                    boss.center_x += 30

                if self.frame_count % 60 == 0:

                    boss.center_x -= 30
                    boss.center_y -= 50
                if self.frame_count % 120 == 0:
                    boss.center_x += 30

            changed = False

            # Scroll left

            # Scroll up
            top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
            if self.player.top > top_bndry:
                self.view_bottom += self.player.top - top_bndry
                changed = True
            bottom_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
            if self.player.top < top_bndry:
                self.view_bottom += self.player.top - top_bndry
                changed = True


            # Scroll down

            # If we need to scroll, go ahead and do it
            # .
            if changed:
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)
            if self.frame_count % 120 == 0:
                powerup = arcade.Sprite("images/powerup.png", BULLET_SCALE)
                powerup.center_x = random.randrange(100, 400)
                powerup.center_y = self.player.center_y + 200
                self.powerup_list.append(powerup)
                self.all_sprites_list.append(powerup)

            if self.POWERED_UP:
                if self.frame_count2 % 100 == 0:
                    self.POWERED_UP = False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.GAME_OVER or self.WIN:
            if self.POWERED_UP:
                bullet = arcade.Sprite("images/bullet.png", BIGBULLET_SCALE)
                bullet.center_x = self.player.center_x
                bullet.angle = 0
                bullet.top = self.player.center_y + 130
                bullet.change_y = 3
                self.bullet_list.append(bullet)
                self.all_sprites_list.append(bullet)
            if not self.POWERED_UP:
                bullet = arcade.Sprite("images/bullet.png", BULLET_SCALE)
                bullet.center_x = self.player.center_x
                bullet.angle = 0
                bullet.top = self.player.top + 60
                bullet.change_y = + 3
                self.bullet_list.append(bullet)
                self.all_sprites_list.append(bullet)

    def on_key_press(self, key, modifiers):
        if self.GAME_OVER:
            if key == arcade.key.SPACE:
                self.GAME_OVER = False
                self.setup()
        if self.WIN:
            if key == arcade.key.SPACE:
                self.GAME_OVER = False
                self.setup()
        if self.GAME_OVER:
            if key == arcade.key.Q:
                exit()
        if not self.GAME_OVER or self.WIN:
            if key == arcade.key.A:
                self.player.center_x -= 62
            if key == arcade.key.D:
                self.player.center_x += 62


def main():
    st = arcade.load_sound("images/Song.mp3")
    arcade.play_sound(st)
    Class()
    arcade.run()


if __name__ == "__main__":
    main()
