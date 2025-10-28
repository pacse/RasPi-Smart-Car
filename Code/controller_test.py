from Server.controller import *

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    CAR = car()
    CAR.display()
