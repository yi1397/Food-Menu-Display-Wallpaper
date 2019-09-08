from appJar import gui
from wallpaper import main


def save():
    try:
        list = app.getAllEntries()
        f = open(r"C:\wallpaper_changer\set.txt", 'w')
        for i in list:
            f.write(i+' =' + str(int(list[i])) + '\n')
        f.write('box_color =khaki\n')
        main()
    except:
        reset()



def reset():
    f = open(r"C:\wallpaper_changer\set.txt", 'w')
    f.write('box_x1 =1350\nbox_x2 =1850\nbox_y1 =100\nbox_y2 =1050\nbox_color =khaki\nfont_size =36\n')


def setting():
    app.go()
    return 1

app = gui('appFirst')
app.setSize(400, 300)
app.addLabel('l_x1', 'x1:', 0, 0, 3)
app.addEntry('box_x1', 0, 3)
app.setEntry('box_x1', '1350')
app.addLabel('l_x1_2', '', 0, 4)
app.addLabel('l_y1', 'y1:', 1, 0, 3)
app.addEntry('box_y1', 1, 3)
app.setEntry('box_y1', '100')
app.addLabel('l_x2', 'x2:', 2, 0, 3)
app.addEntry('box_x2', 2, 3)
app.setEntry('box_x2', '1850')
app.addLabel('l_y2', 'y2:', 3, 0, 3)
app.addEntry('box_y2', 3, 3)
app.setEntry('box_y2', '1050')
app.addLabel('l_f', 'font size:', 4, 0, 3)
app.addEntry('font_size', 4, 3)
app.setEntry('font_size', '36')
app.addButton('save', save, 5, 1)
app.addButton('reset', reset, 5, 2)


setting()