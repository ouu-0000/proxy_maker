import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import glob
import math
#ウィンドウ上部:デッキリスト(40),, page数 
#ウィンドウ下部:カード6枚くらい, button 左右, page数
#その他機能:カードサイズ選択, button　印刷->画像生成
root = tk.Tk()
root.title("print_card")
root.geometry("1000x1000")
deck = []
#input folder image
folder_path = '.\\card_list'
file_list = []
file_list_png = []
file_list_jpeg = []
file_list_jpg = []
if len(glob.glob("./card_list/*.png")) != 0:
    file_list_png = glob.glob("./card_list/*.png")
if len(glob.glob("./card_list/*.jpeg")) != 0:
    file_list_jpeg = glob.glob("./card_list/*.jpeg")
if len(glob.glob("./card_list/*.jpg")) != 0:
    file_list_jpg = glob.glob("./card_list/*.jpg")

for file in file_list_png:
    file_list.append(file)
for file in file_list_jpeg:
    file_list.append(file)
for file in file_list_jpg:
    file_list.append(file)

images = list()
photos = list()

for file in file_list:
    file = str(file).replace('\\', '/')
    image = Image.open(str(file))
    image = image.resize((63, 88))
    images.append(image)
    photos.append(ImageTk.PhotoImage(image))

card_index = 0
# label = tk.Label(root, text='Hello Python')


# canvas.bind("<Button-1>", lambda event: print("画像がクリックされました！"))
def display():
    canvas = tk.Canvas(root, width=1000, height=1000)#width=210, height=297
    canvas.place(x=0, y=0)
    button_card_left = tk.Button(text='左', width=1, height=1)
    button_card_right = tk.Button(text='右', width=1, height=1)
    button_save = tk.Button(text='保存', width=2, height=1)
    button_save.bind("<Button-1>", save_deck)
    button_card_left.bind("<Button-1>", card_left)
    button_card_right.bind("<Button-1>", card_right)
    #display deck_list
    x = 63/2+20
    y = 88/2
    for i in range(0, 40):
        if i < len(deck):
            image_card = photos[deck[i]]
            canvas.create_image(x, y, image=image_card)
            if x >= 63*7+63/2+20 and y <=88*4+88/2:
                x = 63/2+20
                y += 88
            else:
                x += 63
            
    #display card_list
    x = 63/2+20
    y = 88*5+88/2+50
    for i in range(0, 6):
        if card_index*6+i < len(photos):
            photo = photos[card_index*6+i]
            canvas.create_image(x, y, image=photo)
            if x <= 63*5+20:
                x += 63
    canvas.bind("<Button-1>", on_image_click)
    button_card_left.place(x=0, y=88*5+88/2+50)
    button_card_right.place(x=63*8+20, y=88*5+88/2+50)
    button_save.place(x=600, y=600)


def add_deck(i):
    if len(deck) < 40:
        deck.append(i)
    display()

def delete_deck(i):
    if len(deck) > i-1:
        del deck[i]
    display()

def card_right(event):
    global card_index
    if card_index < (len(photos)/6)-1:
        card_index += 1
    display()

def card_left(event):
    global card_index
    if card_index > 0:
        card_index -= 1
    display()

def save_deck(event):    #width=210, height=297
    images_big = list()
    for file in file_list:
        file = str(file).replace('\\', '/')
        image = Image.open(str(file))
        image = image.convert("L")
        images_big.append(image)
    im = []
    x = 0
    y = 0
    im_index = 0
    for i in range(0, math.ceil(len(deck)/9)):
        im.append(Image.new("RGB", (2894, 4093), (255,255,255)))
    for i in range(0, 40):
        if i < len(deck):
            im[im_index].paste(images_big[deck[i]].resize((868, 1213), resample=Image.LANCZOS), (x, y))
            if x >= 868*2 and y >= 1213*2:
                im_index += 1
                x = 0
                y = 0
            elif x >= 868*2:
                x = 0
                y += 1213
            else :
                x += 868
    for i in range(0, len(im)):
        im[i].save('.\\output_deck\\deck'+str(i)+'.png', quality=95)


def on_image_click(event):
    x, y = event.x, event.y
    click_card = -1
    click_card_x = -1
    click_card_y = -1
    if y <= 88*6+50 and y >= 88*5+50:
        for i in range(6, -1, -1):
            if x <= 63*i+63/2:
                click_card = i-1
        if click_card != -1 and card_index*6+click_card < len(photos):
            add_deck(card_index*6+click_card)
    elif y >= 0 and y <= 88*5:
        for i in range(8, -1, -1):
            if x <= 63*i+20:
                click_card_x = i-1
        for i in range(5, -1, -1):
            if y <= 88*i:
                click_card_y = i-1
        if click_card_x != -1 and click_card_y != -1 and click_card_x+click_card_y*8 < len(deck):
            delete_deck(click_card_x+click_card_y*8)
    print(f"クリック位置: ({x}, {y})")
    display()

display()
root.mainloop()
