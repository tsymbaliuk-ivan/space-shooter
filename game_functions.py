import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from star import Star
from random import randint


# events
def check_keydown_event(event, ai_settings, screen, ship, bullets, shot_sound):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, shot_sound)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, scoreboard_, play_button, ship, aliens, bullets, shot_sound):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard_, play_button, ship, aliens, bullets, mouse_x,
                              mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets, shot_sound)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def check_aliens_bottom(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets)


def check_play_button(ai_settings, screen, stats, scoreboard_, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()

        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

        # Сброс игровой статистики.
        stats.reset_stats()
        stats.game_active = True

        # Сброс изображений счетов и уровня.
        scoreboard_.prep_score()
        scoreboard_.prep_high_score()
        scoreboard_.prep_level()
        scoreboard_.prep_ships()

        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_high_score(stats, scoreboard_):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard_.prep_high_score()


def update_screen(ai_settings, screen, stats, scoreboard_, ship, bullets, aliens, play_button, stars):
    """Update images on the screen and flip to the new screen."""

    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    ship.blitme()
    aliens.draw(screen)


    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    scoreboard_.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets, explosion_sound):
    """Update position of bullets, and get rid of old bullets."""
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collicions(ai_settings, screen, stats, scoreboard_, ship, bullets, aliens, explosion_sound)


def check_bullet_alien_collicions(ai_settings, screen, stats, scoreboard_, ship, bullets, aliens, explosion_sound):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    # Проверка попаданий в пришельцев.
    # При обнаружении колизии удалим пулю и пришельца.

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        explosion_sound.play()

        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard_.prep_score()
            check_high_score(stats, scoreboard_)

    if len(aliens) == 0:
        # Если весь флот уничтожен, начинается следующий уровень.
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня
        ai_settings.increase_speed()
        stats.level += 1
        scoreboard_.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets,shot_sound):
    """Выпускает пулю, если максимум еще не достигнут."""

    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        shot_sound.play()


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    numeber_aliens_x = int(available_space_x / (2 * alien_width))

    return numeber_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""

    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""

    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Создание первого ряда пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.ships_left > 0:
        # Уменьшение ships_left.
        stats.ships_left -= 1
        # Обновление игровой информации.
        scoreboard_.prep_ships()
        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets)
    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets)


# About stars
def get_number_stars_x(ai_settings, star_width):
    """Вычисляет количество звезд в ряду."""
    available_space_x = ai_settings.screen_width  # - 2 * star_width
    number_stars_x = int((available_space_x / (4 * star_width)))

    return number_stars_x


def get_number_rows_for_star(ai_settings, star_height):
    """Определяет количество рядов, помещающихся на экране."""

    available_space_y = (ai_settings.screen_height - 2 * star_height)
    number_rows = int(available_space_y / (2 * star_height))

    return number_rows


def create_star(ai_settings, screen, stars, star_number):  # , row_number):
    """Создает пришельца и размещает его в ряду."""
    star = Star(ai_settings, screen)
    star_width = star.rect.width
    star.x = star_width + 5 * star_number * star_width
    star.y = randint(-500, 500)
    star.rect.x = star.x

    star.rect.y = star.rect.height + 5 * star.rect.height  # * row_number
    # Randomize the positions of the stars.
    #  This effect looks much better with a tiny star. If you're curious,
    #  you might want to play around with the spacing a little.
    star.rect.x += randint(-50, 50)
    star.rect.y += randint(-20, 20)

    stars.add(star)


def create_stars(ai_settings, screen, stars):
    """Create a full fleet of aliens."""
    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
    for star_number in range(number_stars_x):
        # Создание star и размещение его в ряду.
        create_star(ai_settings, screen, stars, star_number)  # ,row_number)


def update_stars(stars, ai_settings):
    stars.update()
    # Удаление star, вышедших за край экрана.
    for star in stars.copy():
        if star.rect.bottom >= ai_settings.screen_width:
            stars.remove(star)
