
from tkinter import PhotoImage
import window as myui
import UnofficialCricbuzzApi as api


def UpdateTeamsLogo(SelectdMatch):
  
    try:
        team1Name=SelectdMatch['team1Name']
        myui.img0 = PhotoImage(file = f"images/{team1Name}.png")
        if myui.img0 is not None:
            myui.canvas.itemconfig(myui.team1_logo,image=myui.img0)

        team2Name=SelectdMatch['team2Name']    
        myui.img1 = PhotoImage(file = f"images/{team2Name}.png")
        if myui.img1 is not None:
            myui.canvas.itemconfig(myui.team2_logo,image=myui.img1)
    except:
        nameIssue =f"images/{team1Name}.png not found.."
        print(nameIssue)

        
def UpdateUserInterface():
    global AllMatches,selectedVs
    print(selectedVs)
    if selectedVs == '':
        return

   
    
    SelectdMatch = api.GetSelectdMatch(AllMatches,selectedVs)
    matchId = SelectdMatch['matchId']

    matchTitle = SelectdMatch['team1Name'] +" vs "+ SelectdMatch['team2Name']
    myui.canvas.itemconfig(myui.title_text,text=matchTitle.upper())

    # match=api.CallMatchDetailsApi(matchId)

    oversData=api.CallApiGetBowlers(matchId)
    scorecard = api.GetScorecard(oversData)
    runrate = api.GetRunrate(oversData)
    matchStatus = api.GetMatchStatus(oversData)
    print(scorecard)
    print(runrate)
    print(matchStatus)
    bowler1 = api.GetLastBowler(oversData)
    print(bowler1)
    bowler2  =api.GetSecondLastBowler(oversData)
    print(bowler2)
    batsman1 = api.GetBatsman1(oversData)
    print(batsman1)

    batsman2  =api.GetBatsman2(oversData)
    print(batsman2)

    lastBall = api.GetLastBall(oversData)
    
    
    
    myui.canvas.itemconfig(myui.score_text,text=scorecard)
    myui.canvas.itemconfig(myui.required_rr_text,text=runrate)
    myui.canvas.itemconfig(myui.matchstatus_text,text=matchStatus)
    myui.canvas.itemconfig(myui.bowler1_text,text=bowler1)
    myui.canvas.itemconfig(myui.bowler2_text,text=bowler2)
    
    myui.canvas.itemconfig(myui.batsman1_text,text=batsman1)
    myui.canvas.itemconfig(myui.batsman2_text,text=batsman2)
    myui.canvas.itemconfig(myui.lastBall_text,text=lastBall)

    lastOutD = api.LastOutBatsman(oversData)
    myui.canvas.itemconfig(myui.partnership_text,text=lastOutD)

    UpdateTeamsLogo(SelectdMatch)


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



