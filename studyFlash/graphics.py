import curses
import time

class Textbox:
    def __init__(self, window, debug=False):
        self.w = window
        self.w.keypad(True)
        self.debug = debug
        self.maxyx = self.w.getmaxyx()
        self.maxindex = self.__calculateIndex(self.w.getmaxyx())
        self.save = [""]*self.maxindex
        self.buffer = ""

    # Get current user input
    def getSaveStr(self):
        savestr = ""
        for s in self.save:
            savestr += str(s)
        return savestr

    # Calculate index corresponding to character position
    def __calculateIndex(self, yx):
        m = self.maxyx
        return yx[1] + m[1]*(yx[0])

    # Calculate position with corresponding index as argument
    def __calculatePos(self, index):
        m = self.maxyx
        y = index // m[1]
        x = (index % m[1])
        return [y, x]

    # Move cursor to the right
    def __moveRight(self):
        t = self.w.getyx()
        if 0 < t[1]+1 < self.maxyx[1] and self.__calculateIndex(t) < len(self.getSaveStr()):
            self.w.move(t[0], t[1]+1)
        elif t[1]+1 == self.maxyx[1] and 0 < t[0]+1 < self.maxyx[0]:
            self.w.move(t[0]+1, 0)

    # Move cursor to the left
    def __moveLeft(self):
        t = self.w.getyx()
        if 0 < t[1] < self.maxyx[1]:
            self.w.move(t[0], t[1]-1)
        elif t[1] == 0 and 0 < t[0] < self.maxyx[0]:
            self.w.move(t[0]-1, self.maxyx[1]-1)

    # Move cursor up
    def __moveUp(self):
        t = self.w.getyx()
        if 0 < t[0] < self.maxyx[0]:
            self.w.move(t[0]-1, t[1])

    # Move cursor down
    def __moveDown(self):
        t = self.w.getyx()
        if 0 < t[0]+1 < self.maxyx[0] and self.__calculateIndex([t[0]+1,t[1]]) < len(self.getSaveStr())+1:
            self.w.move(t[0]+1, t[1])
        self.buffer = ""
    
    # Move curser to end of user input 
    def __moveEnd(self):
        lenght = len(self.getSaveStr())
        yx = self.__calculatePos(lenght)
        self.w.move(yx[0], yx[1])

    # Delete character before cursor
    def __delete(self):
        t = self.w.getyx()
        if 0 < t[1] < self.maxyx[1]:
            self.w.move(t[0], t[1]-1)
            self.w.delch(t[0], t[1]-1)
            key = self.__calculateIndex([t[0],t[1]-1])
        elif t[1] == 0 and 0 < t[0] < self.maxyx[0]:
            self.w.move(t[0]-1, self.maxyx[1]-1)
            self.w.delch(t[0]-1, self.maxyx[1]-1)
            key = self.__calculateIndex([t[0]-1,t[1]-1])
        else:
            return
        pos = self.w.getyx()
        self.save = self.save[:key] + self.save[key+1:] + [""]
        self.w.erase()
        self.w.addstr(0,0,self.getSaveStr())
        # move to previous position
        self.w.move(pos[0], pos[1])
    
    # Insert character in textfield
    def __insert(self, string):
        pos = self.w.getyx()
        i = self.__calculateIndex(pos)
        self.save = self.save[:i] + [string] + self.save[i:-1]
        self.w.erase()
        if self.debug:
            self.w.addstr(2,0,str(i))
            self.w.move(pos[0], pos[1])
        self.w.addstr(0,0,self.getSaveStr())
        self.w.move(pos[0], pos[1])
    
    # Get user input
    def gather(self):
        while True:
            char = self.w.getch()
            if char == curses.KEY_RIGHT:
                self.__moveRight()
            elif char == curses.KEY_LEFT:
                self.__moveLeft()
            elif char == curses.KEY_UP:
                self.__moveUp()
            elif char == curses.KEY_DOWN:
                self.__moveDown()
            elif char == curses.KEY_HOME or char == 546:
                self.w.move(0,0)
            elif char == curses.KEY_END or char == 561:
                self.__moveEnd()
            elif char == curses.KEY_BACKSPACE or char == 127:
                self.__delete()
            elif char == 10 or char == curses.KEY_ENTER:
                break
            else:
                # print(char)
                self.buffer += str(hex(char)[2:])
                try:
                    string = bytes.fromhex(self.buffer).decode("utf-8")
                    self.__insert(string)
                    self.__moveRight()
                    self.buffer = ""
                except:
                    pass
        self.w.refresh()
        
        return self.getSaveStr()