import winreg as w
from tkinter import Tk, Frame, Button, BOTH, SUNKEN, colorchooser
from tkinter import messagebox as mb
# 204 204 255
global color
color = (0, 0, 0)
keyValue = "Control Panel\\Colors"

class Window(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Смена выделения")
        self.pack(fill=BOTH, expand=1)

        self.btn = Button(self, text="Выберите цвет", command=self.onChoose, width=15)
        self.btn.place(x=12.5, y=130)

        self.btn = Button(self, text="Установить цвет", command=self.onSet, width=15)
        self.btn.place(x=12.5, y=160)

        self.frame = Frame(self, border=1, relief=SUNKEN, width=100, height=100)
        self.frame.place(x=20, y=20)

    def onChoose(self):
        global color

        (rgb, hx) = colorchooser.askcolor()
        color = rgb
        self.frame.config(bg=hx)

    def onSet(self):
        global color

        if color != (0, 0, 0):
            value = ' '.join(map(str, color))
            key = w.OpenKey(w.HKEY_CURRENT_USER, keyValue, 0, w.KEY_ALL_ACCESS)
            w.SetValueEx(key, 'Hilight', None, w.REG_SZ, value)
            w.SetValueEx(key, 'HotTrackingColor', None, w.REG_SZ, value)
            print(value)
            w.CloseKey(key)
            Window.onInfo(self)
        else:
            Window.onError(self)

    def onInfo(self):
        mb.showinfo("Ифнормация", "Цвет изменен, перезагрузите компьютер.")

    def onError(self):
        mb.showerror("Ошибка", "Для начала выберите цвет.")


def main():

    root = Tk()
    ex = Window()
    root.resizable(width=False, height=False)
    root.geometry("140x200")


    def on_mouse_down(event):
        global dif_x, dif_y
        win_position = [int(coord) for coord in root.wm_geometry().split('+')[1:]]
        dif_x, dif_y = win_position[0] - event.x_root, win_position[1] - event.y_root

    def update_position(event):
        root.wm_geometry("+%d+%d" % (event.x_root + dif_x, event.y_root + dif_y))

    root.bind('<ButtonPress-1>', on_mouse_down)
    root.bind('<B1-Motion>', update_position)

    root.mainloop()

if __name__ == '__main__':
    main()