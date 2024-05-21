from tkinter import messagebox, Tk, Canvas, PhotoImage, HIDDEN
import random
import time.sleep




class Game:
    def __init__(self):
        self.tk=Tk()
        self.tk.title("Stick man escape")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas=Canvas(self.tk, width=500, height=500, \
                highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height=500
        self.canvas_width=500
        self.bg=PhotoImage(file="background.gif")
        w=self.bg.width()
        h=self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h, \
                        image=self.bg, anchor='nw')
        self.sprites=[]
        self.running=True
        self.gameOverFrame=0

    def mainloop(self):
        while 1:
            # 游戏进行中（running == True）
            if self.running==True:
                for sprite in self.sprites:
                    sprite.move()

            # 游戏结束（火柴人遇到门）
            else:
                door.open()
                self.tk.update_idletasks()
                self.tk.update()
                time.sleep(1)
                sf.hide()
                self.tk.update_idletasks()
                self.tk.update()
                time.sleep(1)
                door.close()
                self.tk.update_idletasks()
                self.tk.update()
                messagebox.showinfo("Game Over!","游戏结束")
                break

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.016)

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

def within_x(co1, co2):
    if(co1.x1>co2.x1 and co1.x1<co2.x2)\
           or(co1.x2>co2.x1 and co1.x2<co2.x2)\
           or(co2.x1>co1.x1 and co2.x1<co1.x2)\
           or(co2.x2>co1.x1 and co2.x2<co1.x1):
       return True
    else:
       return False

def within_y(co1, co2):
    if(co1.y1>co2.y1 and co1.y1<co2.y2)\
           or(co1.y2>co2.y1 and co1.y2<co2.y2)\
           or(co2.y1>co1.y1 and co2.y1<co1.y2)\
           or(co2.y2>co1.y1 and co2.y2<co1.y1):
       return True
    else:
        return False

def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x2<=co2.x2 and co1.x1>=co2.x1:
            return True
    return False

def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2>=co2.x1 and co1.x2<=co2.x2:
            return True
    return False

def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1<=co2.y2 and co1.x2>=co2.x2:
            return True
    return False

def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc=co1.y2+y
        if y_calc>=co2.y1 and y_calc<=co2.y2:
            return True
    return False

class Sprite:
    def __init__(self, game):
        self.game=game
        self.isDoor=False
        self.coordinates=None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image=photo_image
        self.image=game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw')
        self.coordinates=Coords(x, y, x+width, y+height)

class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left=[
            PhotoImage(file="stick-L1.gif"),
            PhotoImage(file="stick-L2.gif"),
            PhotoImage(file="stick-L3.gif")
        ]
        self.images_right=[
            PhotoImage(file="stick-R1.gif"),
            PhotoImage(file="stick-R2.gif"),
            PhotoImage(file="stick-R3.gif")
        ]
        self.image=game.canvas.create_image(200, 470, \
                image=self.images_left[0], anchor='nw')
        self.x= -2
        self.y= 0
        self.current_image= 0
        self.current_image_add= 1
        self.jump_count= 0
        self.last_time=time.time()
        self.coordinates=Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y==0:
            self.x= -2

    def turn_right(self, evt):
        if self.y==0:
            self.x=2

    def jump(self, evt):
        if self.y==0:
            self.y= -10
            self.jump_count=0

    # 当小人向左（x<0）或向右（x>0）移动时，不停切换小人的图片，让小人看起来在跑动
    def animate(self):
        if self.x!=0 and self.y==0:
        #if self.x!=0
            # 当时间经过了0.1秒时，更新小人应该使用的图片的下标，
            # 下标不断地在 0, 1, 2, 1, 0, 1, 2, 1, 0 这样循环
            if time.time()-self.last_time>0.1:
                self.last_time=time.time()
                self.current_image+=self.current_image_add
                if self.current_image>=2:
                    self.current_image_add= -1
                if self.current_image<=0:
                    self.current_image_add= 1
        if self.x<0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_left[self.current_image])
        elif self.x>0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                        image=self.images_right[self.current_image])
                
    def coords(self):
        # x=横向移动，y=竖向移动，x的起始点是左面，y的起始点是上面
        xy=self.game.canvas.coords(self.image)
        # print(xy)
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+27
        self.coordinates.y2=xy[1]+30           
        return self.coordinates
    
    def move(self):
        self.animate()

        # return
        if self.y<0:
            self.jump_count+= 1
            if self.jump_count>20:
                self.y=4
        if self.y>0:
            self.jump_count-= 1

        # co 是火柴人当前的坐标
        co=self.coords()
        left=True
        right=True
        top=True
        bottom=True
        falling=True

        # 这个放在后面去理解
        if self.y>0 and co.y2>=self.game.canvas_height:
            self.y=0
            bottom=False
        elif self.y<0 and co.y1<=0:
            self.y=0
            top=False
        if self.x>0 and co.x2>=self.game.canvas_width:
            self.x=0
            right=False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        for sprite in self.game.sprites:
            # 如果遇到自己（火柴人）那么跳过下面的代码
            if sprite == self:
                continue

            # 当前这个精灵的坐标(x1,y1),(x2,y2)
            sprite_co = sprite.coords()
            
            # 
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            
            #
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            
            #print(bottom, falling, self.y)
            
            #
            if bottom and falling and self.y == 0 \
                        and co.y2 < self.game.canvas_height \
                        and collided_bottom(1, co, sprite_co):
                falling = False

            #
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.isDoor:
                    self.game.running = False
            
            #
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.isDoor:
                    self.game.running = False

        if falling and bottom and self.y == 0 \
                and co.y2 < self.game.canvas_height:
            self.y = 4

        #print('方向', self.x, self.y)
        self.game.canvas.move(self.image, self.x, self.y)

    def hide(self):
        self.game.canvas.itemconfig(self.image, state=HIDDEN)

class DoorSprite(Sprite):
    def __init__(self, game, closed_image, opened_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.closed_image = closed_image
        self.opened_image = opened_image
        self.image = game.canvas.create_image(x, y, image=self.closed_image, anchor='nw')
        self.coordinates = Coords(x, y, x + (width / 2), y + height)
        self.isDoor = True
        #self.open()

    def open(self):
        self.game.canvas.itemconfig(self.image, image=self.opened_image)

    def close(self):
        self.game.canvas.itemconfig(self.image, image=self.closed_image)

g = Game()
platfrom1 = PlatformSprite(g, PhotoImage(file = "platform1.gif"), 0, 480, 100, 10)
platfrom2 = PlatformSprite(g, PhotoImage(file = "platform1.gif"), 150, 440, 100, 10)
platfrom3 = PlatformSprite(g, PhotoImage(file = "platform1.gif"), 300, 400, 100, 10)
platfrom4 = PlatformSprite(g, PhotoImage(file = "platform1.gif"), 300, 160, 100, 10)
platfrom5 = PlatformSprite(g, PhotoImage(file = "platform2.gif"), 175, 350, 66, 10)
platfrom6 = PlatformSprite(g, PhotoImage(file = "platform2.gif"), 50, 300, 66, 10)
platfrom7 = PlatformSprite(g, PhotoImage(file = "platform2.gif"), 170, 120, 66, 10) # platfrom7 是门的右下那个平台
platfrom8 = PlatformSprite(g, PhotoImage(file = "platform1.gif"), 45, 60, 100, 10)
platfrom9 = PlatformSprite(g, PhotoImage(file = "platform2.gif"), 170, 250, 32, 10)
platfrom10 = PlatformSprite(g, PhotoImage(file = "platform2.gif"), 230, 200, 32, 10)
g.sprites.append(platfrom1)
g.sprites.append(platfrom2)
g.sprites.append(platfrom3)
g.sprites.append(platfrom4)
g.sprites.append(platfrom5)
g.sprites.append(platfrom6)
g.sprites.append(platfrom7)
g.sprites.append(platfrom8)
g.sprites.append(platfrom9)
g.sprites.append(platfrom10)

door = DoorSprite(g, PhotoImage(file="door-closed.gif"), PhotoImage(file="door-opened.gif"), 45, 30, 40, 35)
g.sprites.append(door)

sf = StickFigureSprite(g)
g.sprites.append(sf)

g.mainloop()

# print("1")
