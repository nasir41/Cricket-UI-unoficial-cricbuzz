from tkinter import *



def CreateDropDown(root,options,MatchSelected):
    drop = OptionMenu( root , clicked , *options ,command=MatchSelected)
    drop.pack(side=TOP, anchor=NW)
    drop.config(bg='aquamarine')
    clicked.set(options[0])
    return drop


window = Tk()
clicked = StringVar()
window.geometry("787x707")
window.configure(bg = "#00cb10")
canvas = Canvas(
    window,
    bg = "#00cb10",
    height = 707,
    width = 787,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"images/background.png")
background = canvas.create_image(
    393.5, 353.5,
    image=background_img)

img0 = PhotoImage(file = f"images/img0.png")
team1_logo = canvas.create_image(
    180, 120,
    image=img0)


img1 = PhotoImage(file = f"images/img1.png")
team2_logo = canvas.create_image(
    600, 120,
    image=img1)



matchstatus_text=canvas.create_text(
    385.5, 212.0,
    text = "Pakistan have won the toss and elected to feild first!\nPlay in Progress!",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(20.0)))

lastBall_text=canvas.create_text(
    385.5, 250,
    text = "",
    fill = "#481c1c",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(15.0)))

partnership_text=canvas.create_text(
    392.0, 490.0,
    text = "0",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(20.0)))

batsman1_text=canvas.create_text(
    163.5, 471.0,
    text = "33\n(14)\nbatsman1_text",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(18)))

batsman2_text=canvas.create_text(
    627.5, 471.0,
    text = "33\n(14)\nbatsman2_text",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(18)))

bowler1_text=canvas.create_text(
    141.5, 626.0,
    text = "33\n(14)\nbowler1_text",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(18)))

bowler2_text=canvas.create_text(
    605.5, 626.0,
    text = "33\n(14)\nbowler2_text",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(18)))

score_text=canvas.create_text(
    374.0, 314.5,
    text = "IND   128/9   (12)",
    fill = "#481c1c",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(40))
    )

required_rr_text=canvas.create_text(
    380.5, 371.0,
    text = "Required Run Rate 4.33",
    fill = "#481c1c",
    font = ("Alatsi-Regular", int(20.0)))


title_text=canvas.create_text(
    391.5, 36.5,
    text = "PAKISTAN VS INDIA",
    fill = "#ffffff",
    anchor=CENTER,
    justify= CENTER,
    font = ("Alatsi-Regular", int(30.0)))

window.resizable(False, False)
# window.mainloop()

