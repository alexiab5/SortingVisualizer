import pygame
import random
import math
pygame.init()

class DrawInformation: 
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    PINK = 255, 0, 77
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst): # initializeaza fereastra aplicatiei cu dimensiunile specificate impreuna cu sirul de valori asociat
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height)) # genereaza fereastra propriu-zisa
        pygame.display.set_caption("Sorting Algorithm Visualiser")
        self.set_list(lst)
    
    def set_list(self, lst): # calculeaza dimensiunile blocurilor in functie de dimensiunile ferestrei, lungimea vectorului si range-ul de valori
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst) 

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending): # deseneaza antetul in functie de metoda de sortare aleasa de utilizator 
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.PINK)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False): # deseneaza pe ecran blocurile coresp valorilor numerice in trei nunate de gri
	lst = draw_info.lst

	if clear_bg: # reseteaza ecranul (doar partea cu blocurile)
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg: # se redeseneaza ecranul pentru fiecare swap din timpul sortarii
		pygame.display.update()

def generate_starting_list(n, min_val, max_val): # genereaza un sir de n valori aleatorii, cuprinse intre min_val si max_val
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        j = i - 1
        while j >= 0 and ((current < lst[j] and ascending) or (current > lst[j] and not ascending)):
            lst[j + 1] = lst[j]
            j = j - 1
            draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
            yield True
        lst[j + 1] = current

    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)):
        k = i
        for j in range (i + 1, len(lst)):
            if(ascending and lst[j] < lst[k]):
                k = j
            elif(not ascending and lst[j] > lst[k]):
                k = j
        aux = lst[i]
        lst[i] = lst[k]
        lst[k] = aux
        draw_list(draw_info, {i: draw_info.GREEN, k: draw_info.RED}, True)
        yield True
    return lst        

def main():
    run = True
    clock = pygame.time.Clock()
   
    n = 60
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val) # sirul initial

    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run: # bucla infinita, pana cand este inchisa aplicatia
        clock.tick(60) #60 fps - viteza de executie

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        
        for event in pygame.event.get(): # se analizeaza fiecare actiune a utilizatorului
            if event.type == pygame.QUIT:
                run = False # inchide fereastra aplicatiei
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r: # tasta R (reset) genereaza un sir nou de valori
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False  
            elif event.key == pygame.K_SPACE and sorting == False: # tasta SPACE incepe sortarea
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting: # sortare crescatoare
                ascending = True
            elif event.key == pygame.K_d and not sorting: # sortare descrescatoare
                ascending = False
            elif event.key == pygame.K_i and not sorting: 
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting: 
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting: 
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"


    pygame.quit()
        
if __name__ == "__main__": 
    main()