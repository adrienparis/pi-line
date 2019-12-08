import userControls as UC


def mainUI():
    print(u"=====Start pi-Line=====")
    win = UC.WindowUC(u"Pi-Line")
    win.load()

    cpBrd = UC.CupboardUC(win)
    cpBrd.create()
    cpBrd.attach(top=UC.Attach.FORM, bottom=UC.Attach.FORM, left=UC.Attach.FORM, right=UC.Attach.FORM, margin=0)

    win.applyAttach()


print(u"=====Load pi-Line=====")
# print("Merci pilou <3")
# mainUI()
