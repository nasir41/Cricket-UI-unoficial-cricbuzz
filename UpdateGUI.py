
import imp
from tkinter import PhotoImage
import window as myui
import CricAPI as api
import time

def UpdateTeamsLogo(selectedVs):
    tName = selectedVs.split(" vs ")
    if len(tName) == 2:
        team1Name = tName[0]
        team2Name = tName[1]
        print(team1Name)
        print(team2Name)
        try:
            myui.img0 = PhotoImage(file = f"images/{team1Name}.png")
            if myui.img0 is not None:
                myui.canvas.itemconfig(myui.team1_logo,image=myui.img0)
            myui.img1 = PhotoImage(file = f"images/{team2Name}.png")
            if myui.img1 is not None:
                myui.canvas.itemconfig(myui.team2_logo,image=myui.img1)
        except:
            nameIssue =f"images/{team1Name}.png not found.."
            print(nameIssue)
        
def UpdateUserInterface():
    global AllMatches,selectedVs
    print(selectedVs)
    if selectedVs is '':
        return

    myui.canvas.itemconfig(myui.title_text,text=selectedVs)
    Eid = api.GetMatchEid(AllMatches,selectedVs)
    match=api.CallMatchDetailsApi(Eid)
    scorecard = api.GetScorecard(match)
    runrate = api.GetRunrate(match)
    matchStatus = api.GetMatchStatus(match)
    print(scorecard)
    print(runrate)
    print(matchStatus)
    bowler1 = api.GetLastBowler(match)
    print(bowler1)
    bowler2  =api.GetSecondLastBowler(match)
    print(bowler2)
    batsman1 = api.GetBatsman1(match)
    print(batsman1)

    batsman2  =api.GetBatsman2(match)
    print(batsman2)

    lastBall = api.GetLastBall(match)
    
    
    
    myui.canvas.itemconfig(myui.score_text,text=scorecard)
    myui.canvas.itemconfig(myui.required_rr_text,text=runrate)
    myui.canvas.itemconfig(myui.matchstatus_text,text=matchStatus)
    myui.canvas.itemconfig(myui.bowler1_text,text=bowler1)
    myui.canvas.itemconfig(myui.bowler2_text,text=bowler2)
    
    myui.canvas.itemconfig(myui.batsman1_text,text=batsman1)
    myui.canvas.itemconfig(myui.batsman2_text,text=batsman2)
    myui.canvas.itemconfig(myui.lastBall_text,text=lastBall)

    lastOutD = api.LastOutBatsman(match)
    myui.canvas.itemconfig(myui.partnership_text,text=lastOutD)

    UpdateTeamsLogo(selectedVs)


def MatchSelected(arg):
    global AllMatches,selectedVs
    selectedVs = arg
    UpdateUserInterface()

    


AllMatches=api.GetAllMatchesList()
myui.window.title("Rizwan Sports Today")
options = []
for x in AllMatches:
    options.append(x['vs'])

selectedVs = options[0]
drop=myui.CreateDropDown(myui.window,options,MatchSelected)


def update_ip():
    try:
        UpdateUserInterface()
        myui.window.after(50000, update_ip)
    except StopIteration:
        pass

update_ip()


myui.window.mainloop()



