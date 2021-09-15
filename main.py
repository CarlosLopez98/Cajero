import pygame
from pygame.locals import *
from character import Character
from queue import Queue
from threading import Thread
from random import randint
from time import sleep


def add_person(queue: Queue):
    while add:
        sleep(0.006)
        number = randint(1, 1000)
        if queue.count() < 6 and number % 1000 == 0:
            # 1 in 1000 chance for a person to join the queue
            person = Character(pos=(-68, height / 3), scale=4)
            queue.join(person)
            print(f'A person has join the queue with {person.bills} bills.')
    print('No more people!')


def attend_person(queue: Queue):
    global key_pos
    bills_payed = 0
    while attend:
        if not queue.is_empty():
            person = queue.attend()
            if person.attending:
                # maximum 5 bills per person
                while person.bills > 0 and bills_payed < 5:
                    sleep(1)  # Every 1 seconds a person pays a bill
                    person.pay_bill()
                    bills_payed += 1
                    print(f'Person has payed a bill, he has {person.bills} left.')
                bills_payed = 0

                move_forward(queue.elements)
                queue.pop()

                person.attending = False
                # key_pos = [person.goal_pos, *key_pos]
                person.goal_pos = None
                person.x = -68
                # If the person still has bills go back to the queue
                if person.bills > 0:
                    queue.join(person)
                    print(f'Person has return to the queue, he has {person.bills} left.')
                else:
                    print('Person has left the queue.')
    print('No more attending!')


# creation of Queue instance
cola = Queue()

# Threads
add = True
attend = True
add_th = Thread(target=add_person, args=(cola,))
attend_th = Thread(target=attend_person, args=(cola,))
add_th.start()
attend_th.start()

# GUI
pygame.init()

width = 750
height = 450

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cashier SO')

# Font
font = pygame.font.Font(None, 40)
num_users = font.render('0', False, (255, 0, 0))

# ATM
atm = pygame.image.load('res/atm.png')
atm_size = atm.get_size()
atm = pygame.transform.scale(atm, (int(atm_size[0] / 5.55), int(atm_size[1] / 5.55)))
atm_size = atm.get_size()

# characters
users = []

key_pos = [(596, 150), (420, 150), (332, 150), (236, 150), (144, 150), (60, 150)]
attending_pos = (596, 150)


def move_forward(users):
    global key_pos
    pos = users[0].goal_pos
    for i in range(1, 7 if len(users) > 7 else len(users)):
        pos1 = users[i].goal_pos
        users[i].goal_pos = pos
        pos = pos1
    if len(users) < 7:
        key_pos = [pos, *key_pos]


clock = pygame.time.Clock()
FPS = 120
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                pass

    # Re-paint the window
    window.fill('#FFFFFF')

    # Rendering background
    pygame.draw.rect(window, '#ADE1F8', (0, 0, width, height // 2))
    pygame.draw.rect(window, '#B8B8B8', (0, height // 2, width, height // 2))
    # Render a sign that show the number of users in the queue
    pygame.draw.rect(window, '#FFFFFF', (30, 30, 80, 50))
    pygame.draw.rect(window, '#FF0000', (30, 30, 80, 50), 2)
    window.blit(num_users, (66, 44))
    # Rendering atm
    window.blit(atm, (width - atm_size[0], height / 3))

    # render users
    for i in range(len(users)):
        users[i].render(window)

        if len(key_pos) != 0 and users[i].goal_pos is None:
            users[i].walk = True
            users[i].goal_pos = key_pos[0]
            key_pos.pop(0)

        if users[i].walk:
            users[i].move()

        if users[i].get_pos() == users[i].goal_pos:
            users[i].stop()
            if users[i].get_pos() == attending_pos:
                users[i].attending = True

    users = cola.elements  # updating the queue
    num_users = font.render(str(len(users)), False, (255, 0, 0))

    clock.tick(FPS)
    fps = int(clock.get_fps())
    fps_text = font.render(str(fps), False, (255, 255, 255))
    window.blit(fps_text, (width - 50, 1))

    # Update the surface
    pygame.display.update()

add = False
attend = False
pygame.quit()
