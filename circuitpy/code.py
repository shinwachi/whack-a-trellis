# MIT License
# 
# Copyright (c) 2019 Shinichiro Wachi
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import board
import random
import adafruit_trellism4
import audioio
import time

sounds = {"hit": "hit.wav", "loss": "loss.wav"}


# whack-a-mole 6x4

trellis = adafruit_trellism4.TrellisM4Express()


class Numbers():
    # font credits Minimum Alpha
    def __init__(self):
             #000111222333444555666777888999
        z = ['### #  ######  ## ############',
             '# ### ### ### ######   ##### #',
             '# # # #    ####  ## # # # # ##',
             '############  ########  ######']
             #000111222333444555666777888999
        # print(z)

        self.numbers_templ = []
        for idx in range(10):
            _offset = idx * 3
            x = '### # ## ## # #####  #########'
            # print (x[0:3])
            # self.numbers_templ[idx] = [rz[_offset:_offset+3] for rz in z]
            self.numbers_templ.append( [rz [_offset:_offset+3] for rz in z])
        # print (self.numbers_templ)

        # refint = for i in range(9)


    def display_1digit(self, x,digit, xcolor = (50,50,50)):
        for iy, zstr in enumerate(self.numbers_templ[digit]):
            for ix, zchr in enumerate(zstr):
                if zchr == "#":
                    trellis.pixels[x+ix,iy] = xcolor
                else:
                    trellis.pixels[x+ix,iy] = (0,0,0)
    def display_number(self, x, mynumber, xcolor = (50,50,50)):
        century = int(mynumber/100)
        # print(century)
        for i in [z for z in range(century)]:
            trellis.pixels[7,i] = (0,50,0)

        ls2d = mynumber%100
        # print ("ls2d", ls2d)
        for ix, xnum in enumerate(str(ls2d)):

            xnum = int(xnum)

            # print (xnum)
            # print ("ix", ix*4)
            self.display_1digit(ix*4,xnum, xcolor)




numbers = Numbers()





def play_sound(filename):
    with audioio.AudioOut(board.A1, right_channel=board.A0) as audio:
        try:
            with open(filename, "rb") as f:
                wave = audioio.WaveFile(f)
                audio.play(wave)
                while audio.playing:
                    time.sleep(0.005)
        except OSError:
            pass
# set of moles, with (x, y, life)
scores = [0] * 8
class Mole:
    def __init__(self):
        print("hi")
        self.life=100


class Player:
    def __init__(self):
        self.life=8
        self.life_indicators = [(x,y) for x,y in zip([0]*4+[7]*4,[0,1,2,3]*8)]
        self.score=0

    def display_life(self):
        for x, y in self.life_indicators:
            trellis.pixels[x,y] = (0,0,100)

    def damage(self):
        in_game = True
        if self.life > 0:
            px,py = self.life_indicators[8-self.life]
            self.life = self.life-1
            trellis.pixels[px,py] = (0,0,0)


        else:
            in_game = False

        return in_game

    def add_score(self):
        self.score += 1
        # play_sound("hit.wav")


def title_scene(high_score):
    # score screen
    i = 0
    numbers.display_number(0,high_score)

    while True:
        press = set(trellis.pressed_keys)
        for y in [1,3]:
            #trellis.pixels[int(i/50%8),y] = (i%70,70,100)
            # numbers.display_1digit(0,2)

            pass
        if len(press) > 0:
            break
        i += 1

    trellis.pixels.fill((0,0,0))

def game_scene(player_life=8):
    # set life indicators
    player = Player()
    player.display_life()


    moles = set()


    in_game = True

    mole_fade_speed = 500
    frequency = 100.0

    while in_game:
        pressed = set(trellis.pressed_keys)

        # prevent cheating
        if len(pressed)>8:
            pressed = set()
            mole_fade_speed += 50

        nx = None
        ny = None
        if random.randint(0,int(frequency)) <= 0:
            nx = random.randint(1,6)
            ny = random.randint(0,3)

        for x,y,life in moles:
            # if nx == x and ny == y:
            #     nx = None
            k = int(life / 1000)
            if k < 0 :
                k = 0
            trellis.pixels[x,y] = (k,k,k)
            moles.remove ((x,y,life))
            if life > 1 :
                if (x,y) in pressed:
                    trellis.pixels[x,y] = (0, 50 ,0)
                    pressed.remove((x,y))
                    player.add_score()
                    mole_fade_speed += 10
                    frequency -= 0.5

                else:
                    moles.add((x,y, life-mole_fade_speed))
            else:
                #damage
                trellis.pixels[x,y] = (255,k,k)

                in_game = player.damage()

            if x == nx and y == ny:
                nx = None
                ny = None


        if nx:
            moles.add((nx, ny, 100000))
    return player.score

def game_over_scene(score=0, win=False):
    trellis.pixels.fill((0,0,0))
    for i in range (255):
        press = set(trellis.pressed_keys)
        for y in range(4):
            # trellis.pixels[int(i/50%8),y] = (100,0,0)
            if win:
                numbers.display_number(0,score, (i,i,0))
            else:
                numbers.display_number(0,score, (0,0,i))
        if len(press) > 0:
            if win:
                if i > 5:
                    break
            else:
                break
        i += 1

def mainloop():
    high_score = 10
    while True:
        title_scene(high_score)

        score = game_scene()
        if score > high_score:
            high_score = score
            win = True
        else:
            win = False


        game_over_scene(score, win)
        # if win == True:
        #     time.sleep(1)









mainloop()