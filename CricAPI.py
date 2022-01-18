import requests
import json
from tkinter import *

def CallAllMatchesApi():
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"

    querystring = {"Category":"cricket"}

    headers = {
        'x-rapidapi-host': "livescore6.p.rapidapi.com",
        'x-rapidapi-key': "1eab839b95mshd98f74f1e9e31f4p12c777jsn666802c72f65"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    respJson = json.loads(response.text)
    return respJson
def CallMatchDetailsApi(id):
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"

    querystring = {"Eid":id,"Category":"cricket","LiveTable":"false"}

    headers = {
        'x-rapidapi-host': "livescore6.p.rapidapi.com",
        'x-rapidapi-key': "1eab839b95mshd98f74f1e9e31f4p12c777jsn666802c72f65"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    return json.loads(response.text)
def GetAllMatchesList():
    jsonAllMatches=CallAllMatchesApi()
    AllMatches=[]
    for jsonMatch in jsonAllMatches['Stages']:
        match = {}
        match['Sid'] = jsonMatch['Sid']
        match['Snm'] = jsonMatch['Snm']
        
        if jsonMatch['Events'] is not None:
            for e in jsonMatch['Events']:
                nMatch = dict(match)
                nMatch['Eid']=e['Eid']
                nMatch['ECo'] = e['ECo']
                nMatch['EpsL'] = e['EpsL']
                T1= e['T1'][0]['Nm']
                T2 = e['T2'][0]['Nm']
                nMatch['vs'] = f'{T1} vs {T2}'
                AllMatches.append(nMatch)
    
    return AllMatches

def ListAllOvers(match):
   SDInn= match['SDInn']
   lastInnIndex = len(SDInn)-1
   overList = []
   if lastInnIndex >= 0:
        lastInn=SDInn[lastInnIndex]
        Ovr = lastInn['Ovr']
        com = lastInn['Com']
        finalComment=''
        for c in com:
            ballNo=c['Ov']
            detail = c['T']
            # S = c['S']
            finalComment = f'{ballNo}: {detail}'
            overList.append(finalComment)
            
        # for over in Ovr:
        #     overNumber = over['OvN']
        #     bowlerName = over['Onm']
        #     allBalls = over['OvT']
        #     overDetail=''
        #     for ball in allBalls:

   return overList



def GetMatchEid(matches,sVs):
    for x in matches:
        if x['vs'] == sVs:
            Eid = x['Eid']
            return Eid
def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)
# Pak 100/2  (20)
def GetLatestInning(match):
    SDInn = match['SDInn']
    if SDInn is None:
        return None
    maxInn = len(SDInn)
    if maxInn == 0:
        return None
    latestInn = SDInn[maxInn-1]
    return latestInn
    
def GetScorecard(match):
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return ''
    
    score=latestInn['Pt']
    Wk=latestInn['Wk']
    Ov=latestInn['Ov']
    # Rr=latestInn['Rr']
    Team = latestInn['Ti']
    Ov="{:.1f}".format(Ov)
    card = f'{Team} {score}/{Wk}  ({Ov})'
    return card

# Current Run Rate 
def GetRunrate(match):
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return 'Current Run Rate 0'
    
    if 'Rr' not in latestInn:
        return 'Current Run Rate 0'
        
    Rr = latestInn['Rr']
    card = f'Current Run Rate {Rr}'
    return card
def GetMatchStatus(match):
    mStatus = match['ECo']
    return mStatus

def GetBowlerWithOver(match,overNm):
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return ''
    
    if 'Ovr' not in latestInn.keys():
        return ''

    Ovr = latestInn['Ovr']
    if Ovr is None:
        return ''
    if len(Ovr) <= overNm:
        return ''
    Over=Ovr[overNm]
    
    bowlerName = Over['Onm']
    return bowlerName

def GetBowlerWithID(match,ID):
    latestInn=GetLatestInning(match)
    bowler = {}
    if latestInn is None:
        return bowler
    Bow = latestInn['Bow']
    if Bow is None:
        return bowler
    
    bowler=first_true(Bow, None, lambda x: int(x['Pid'])==int(ID))
    return bowler     
def GetBatterWithID(match,ID):
    latestInn=GetLatestInning(match)
    bowler = {}
    if latestInn is None:
        return bowler
    Bow = latestInn['Bat']
    if Bow is None:
        return bowler
    
    bowler=first_true(Bow, None, lambda x: int(x['Pid'])==int(ID))
    return bowler
def GetPersonFromName(match,name):
    Prns= match['Prns']
    person={}
    person=first_true(Prns, None, lambda x: x['Fn'] in name and x['Ln'] in name )
    if person is None:
        person1=first_true(Prns, None, lambda x: x['Fn'] in name )
        if person1 is not None:
            bowler = GetBowlerWithID(match,person1['Pid'])
            if bowler is None:
                person=first_true(Prns, None, lambda x: x['Ln'] in name )
            else:
                person=person1
        else:
            person=first_true(Prns, None, lambda x: x['Ln'] in name )
    return person

def GetPersonFromID(match,ID):
    Prns= match['Prns']
    person = {}
    person=first_true(Prns, person, lambda x: int(x['Pid'])==int(ID))
    return person

def GetBowlerNumber(match,number):
    bowler={}
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return bowler
    Bow = latestInn['Bow']
    if Bow is None:
        return bowler
    if len(Bow) <= number :
        return bowler
    
    return Bow[number]


# bowlername|Score/Wickets (overs)
def GetBowlerStat(bowler):
    name = bowler['name']
    score = bowler['R']
    wickets = bowler['Wk']
    Overs = bowler['Ov']
    # Economy = bowler['Er']
    card = f'{name} \n{score}/{wickets} \n({Overs} ov)'
    return card

def GetBowler0(match):
    bowler = GetBowlerNumber(match,0)
    if bowler is None:
        return None
    
    bowlerPerson = GetPersonFromID(match,int(bowler['Pid']))
    bowler['name'] = bowlerPerson['Fn'] +' '+ bowlerPerson['Ln']
    return GetBowlerStat(bowler)
def GetBowler1(match):
    bowler = GetBowlerNumber(match,1)
    if bowler is None:
        return None
    
    bowlerPerson = GetPersonFromID(match,int(bowler['Pid']))
    bowler['name'] = bowlerPerson['Fn'] +' '+ bowlerPerson['Ln']
    return GetBowlerStat(bowler)
def GetLastBowler(match):
    bowlerName =GetBowlerWithOver(match,0)
    if bowlerName == '':
        return GetBowler0(match)
    else:
        bowlerPerson = GetPersonFromName(match,bowlerName)
        if bowlerPerson is None:
            return GetBowler0(match)
        
        bowler = GetBowlerWithID(match,int(bowlerPerson['Pid']))
        if bowler is None:
            return GetBowler0(match)

        bowler['name'] = bowlerName
        return GetBowlerStat(bowler)
        

def GetSecondLastBowler(match):
    bowlerName =GetBowlerWithOver(match,1)
    if bowlerName == '':
        return GetBowler0(match)
    else:
        bowlerPerson = GetPersonFromName(match,bowlerName)
        if bowlerPerson is None:
            return GetBowler1(match)
        
        bowler = GetBowlerWithID(match,int(bowlerPerson['Pid']))
        if bowler is None:
            return GetBowler1(match)
            
        bowler['name'] = bowlerName
        return GetBowlerStat(bowler)


# batsmanname|Score/ballz |(overs)
def GetBatsmanStat(batsman):
    name = batsman['name']
    score = batsman['R']
#     wickets = batsman['Wk']
    B = batsman['B']
#     Economy = batsman['Er']
    card = f'{name} \n{score} \n({B})'
    return card
# batsmanname|Score/ballz |(overs)
def GetOutBatsmanStat(batsman):
    score = batsman['R']
#     wickets = batsman['Wk']
    B = batsman['B']
#     Economy = batsman['Er']
    card = f'{score} ({B})'
    return card
def GetBatsmanNumber(match,number):
    batsman={}
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return batsman
    Bat = latestInn['Bat']
    if Bat is None:
        return batsman
    if len(Bat) <= number :
        return batsman
    
    batsman=Bat[number]
    return batsman
def GetBatsman1(match):
    batsman={}
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return batsman
    Bat = latestInn['Bat']
    if Bat is None:
        return batsman
    batsman=first_true(Bat, None, lambda x: int(x['Pl'])==1 or x['LpTx']=='not out')
    if batsman is None:
        batsman = GetBatsmanNumber(match,0)
    
    Person = GetPersonFromID(match,int(batsman['Pid']))
    batsman['name'] = Person['Fn'] +' '+ Person['Ln']
    return GetBatsmanStat(batsman)

def GetBatsman2(match):


    batsman={}
    latestInn=GetLatestInning(match)
    if latestInn is None:
        return batsman
    Bat = latestInn['Bat']
    if Bat is None:
        return batsman
    
    count=0
    for b in Bat:
        if int(b['Pl']) == 1 or b['LpTx']=='not out':
            if count==0:
                count=1
            else:
                batsman=b
                break
#     print(batsman)        
    if batsman is None:
        batsman = GetBatsmanNumber(match,1)
    
    if 'Pid' not in batsman.keys():
        return batsman
        
    Person = GetPersonFromID(match,int(batsman['Pid']))
    batsman['name'] = Person['Fn'] +' '+ Person['Ln']
    return GetBatsmanStat(batsman)
def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False
def GetLastBall(match):
    latestInn=GetLatestInning(match)
    ball = ''
    if latestInn is None:
        return ball
    
    if 'Com' not in latestInn:
        return ball
    Com = latestInn['Com']
    if Com is None:
        return ball
    if len(Com) <= 0:
        return ball
    
    lBall = Com[0]
    if 'Ov' not in lBall:
        return ball
    ballNo = lBall['Ov']
    # f = float(ballNo)

    if 'T' not in lBall:
        return ball
    comment = lBall['T']
    # if is_integer_num(ballNo):
    #     ball=f'{comment}'
    #     return ball
    
    ball=f'{comment}'
    return ball

#Last Bat: Nathan McSweeney c Morris b Hatzoglou 6 (6b 1x4 0x6) SR: 100
def LastOutBatsman(match):
    latestInn=GetLatestInning(match)
    ball = ''
    if latestInn is None:
        return ball
    
    if 'FoW' not in latestInn:
        return ball

    Com = latestInn['FoW']
    if Com is None:
        return ball
    if len(Com) <= 0:
        return ball
    
    lBall = Com[0]

    batterid = lBall['Pid']
    batsman = GetBatterWithID(match,batterid)
    batsmanName = GetPersonFromID(match,batterid)
    batname=batsmanName['Fn'] + " "+ batsmanName['Ln']
    bowlerid = lBall['Bid']
    bowler = GetPersonFromID(match,bowlerid)
    bowlname=bowler['Fn'] + " "+ bowler['Ln']
    # outReason = batsman['LpTx']
    scoreCard = GetOutBatsmanStat(batsman)
    # f = float(ballNo)

    comment = f'{batname} {scoreCard} \nb {bowlname}'
   
    return comment