import pygame
import time
import numpy as np
from button import BoolButton
import platform

font = 'stsong' #this will come handy later..
pygame.font.init()

class InputShape:
	def __init__(self, screen, xywh=None):
		if xywh is None:
			xywh = (10, 10, 100, 50)
		self.screen = screen
		self.xywh = xywh
		self.rect = pygame.Rect(*self.xywh)

	# self.big_txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)

	def draw(self):
		pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)

	def onclick(self, x, y):
		return self.xywh[0] < x < self.xywh[0] + self.xywh[2] and self.xywh[1] < y < self.xywh[1] + self.xywh[3]

#class to get free drawn polygon from the user
#maybe we took to much artistic freedom here
def get_points(screen, ask_text=None, skip_chinese=False):
	l = list()
	if ask_text is not None:
		#what text to print on the screen (as instructions)
		# pygame.font.Font(r'C:\WINDOWS\FONTS\MSJH.TTC', 15).render(line, True, (0, 0, 0))
		text_button = BoolButton(pos=(20, 20), size=(1300, 0), color="#FFFFFF", text=ask_text,
										 fg_color="#000000", elevation=0)
		clear_button = BoolButton(pos=(0, 0), size=(250, 50), color="#FFFFFF", text='nothing',
								 fg_color="#FFFFFF", elevation=0)
		text_button.draw(screen)
		pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				#add point to polygon
				l.append(pygame.mouse.get_pos())
				if len(l) > 1:
					pygame.draw.line(screen, (255, 0, 0), l[-1], l[-2])
					pygame.display.update()
			if (skip_chinese and len(l)) or event.type == pygame.KEYDOWN :
				#enter is pressed - finished drawing
				if (skip_chinese and len(l)) or event.key == pygame.K_RETURN: #use early return as feature!!!!
					if len(l) > 2 or skip_chinese:
						#enough points are drawn
						pygame.draw.line(screen, (255, 0, 0), l[0], l[-1])
						clear_button.draw(screen)
						pygame.display.update()
						return np.array(l, dtype=float)
					else:
						#drawn not enough point (less than 2)
						if (platform.system() != 'Windows'):
							#currenctly only windows support chinese text
							creator = 'Torvalds' if (platform.system() == 'Linux') else 'Apple'
							print("You don't use Windows, Bill Gates is sad. At least ", creator, " is happy.")
							print("(BTW, we are shutting this app because of this. We will also shutter your window when you will sleep. Maybe then you will understand the value of windows.)")
							print("P.S - you less points than inteded in draw polygon. That's the real reason we hate you.")
							exit()
						screen.fill((255, 0, 0))
						# text = 'Terriblus Errorum: cantus allocatus 50000000 bytii'
						text = u'''struct.c:8:1: warning: no semicolon at end of struct or union
} book;
^
話說天下大勢，分久必合，合久必分。
寧教我負天下人，休教天下人負我。
人中呂布，馬中赤兔。
蒼天既已生公瑾，塵世何須出孔明？

这是警告提示,提示我们需要在struct和union数据类型定义的后面加上分号;,这样的好处就是当我们需要再添加一个成员变量的时候，只需写上该成员变量的定义,而无需先敲;，我太机智了，手动滑稽...
没有成员变量的结构体

我们也可以定义一个空的结构体，有时候我们需要某一个结构体数据类型，但是暂时又不知道如何填充里面的成员变量，我们可以有如下定义

struct Books {
//TODO
} book;

访问结构体成员

定义完结构体积后接下来就是去访问它并给他赋值，为了访问一个结构体成员变量，我们可以使用成员操作符(.) 成员访问运算符被编码为结构变量名称和我们希望访问的结构成员之间的句点(.)如下所示的完整代码'''
						#translation for the chinese:
						# "The kingdom long united must divide, ling devided must unite"
						# "I would rather betray the world, than let the world betray me" (Cao Cao)
						# "Among men - Lu Bu, Aming steads - Red Hare"
						# "O God, since you made Zhou Yu, why did you also create Zhuge Liang?"
						# Those qoutes are from the Romance of Three kingdoms. The translation is not literal
						# After this, there is an explanation in Chinese about forgetting ; in c
						# font = pygame.font.SysFont(font, 190)
						for i,line in enumerate(text.split('\n')):
							# line = line.encode('utf-8')
							text_surface = pygame.font.Font(r'C:\WINDOWS\FONTS\MSJH.TTC', 15).render(line, True, (0,0,0))
							screen.blit(text_surface, (50, 30+25*i))
						pygame.display.update()
						time.sleep(20)
						pygame.display.quit()
						pygame.quit()
						exit(-1)
