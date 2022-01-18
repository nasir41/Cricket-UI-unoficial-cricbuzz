import requests
import json
def first_true(iterable, default=False, pred=None):

    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)
def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False
def CallAllMatchesApi():
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/list"

    querystring = {"matchState":"live"}

    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': "1eab839b95mshd98f74f1e9e31f4p12c777jsn666802c72f65"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    respJson = json.loads(response.text)
    return respJson
def CallMatchDetailsApi(id):
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"

    querystring = {"matchId":id}

    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': "1eab839b95mshd98f74f1e9e31f4p12c777jsn666802c72f65"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)
def CallApiGetBowlers(id):
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-overs"

    querystring = {"matchId":id}

    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': "1eab839b95mshd98f74f1e9e31f4p12c777jsn666802c72f65"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)    

def GetAllMatchesList():

    AllMatches=[]
    jsonAllMatches=CallAllMatchesApi()
    if 'typeMatches' not in jsonAllMatches:
        return AllMatches

    typeMatches=jsonAllMatches['typeMatches']
    
    for tmatch in typeMatches:
        if tmatch['matchType'] == 'International' or tmatch['matchType'] == 'League':
            if 'seriesAdWrapper' not in tmatch:
                return AllMatches
            seriesAdWrapper=tmatch['seriesAdWrapper']
            for saw in seriesAdWrapper:
                if 'seriesMatches' in saw:
                    seriesMatches= saw['seriesMatches']
                    if 'matches' in seriesMatches:
                        matches= seriesMatches['matches']
                        for match in matches:
                            if 'matchInfo' in match:
                                matchInfo = match['matchInfo']
                                matchId= matchInfo['matchId']
                                team1= matchInfo['team1']
                                team2= matchInfo['team2']
                                MatchDic = {}
                                MatchDic['matchId']=matchId
                                MatchDic['team1Name']=team1['teamName']
                                MatchDic['team2Name']=team2['teamName']
                                MatchDic['vs']=team1['teamSName']+" vs "+team2['teamSName']
                                AllMatches.append(MatchDic)
    
    return AllMatches

def GetMatchEid(matches,sVs):

    for x in matches:
        if x['vs'] == sVs:
            Eid = x['matchId']
            return Eid

def GetLastScorecard(match):
    if 'scorecard' not in match:
        return None
    scorecard=match['scorecard']
    lscorecard = len(scorecard)
    if lscorecard <= 0 :
        return None
    
    lastScorecard=scorecard[lscorecard-1]
    return lastScorecard
    
def GetScorecard1(match):
    scorecard=GetLastScorecard(match)
    if scorecard is None:
        return ''
    
    score=scorecard['score']
    Wk=scorecard['wickets']
    Ov=scorecard['overs']
    # Rr=latestInn['Rr']
    Team = scorecard['batTeamName']
    Ov="{:.1f}".format(Ov)
    card = f'{Team} {score}/{Wk}  ({Ov} Ov)'
    return card
def GetRunrate1(match):
    latestInn=GetLastScorecard(match)
    if latestInn is None:
        return 'Current Run Rate 0'
    
    if 'runRate' not in latestInn:
        return 'Current Run Rate 0'
        
    Rr = latestInn['runRate']
    card = f'Current Run Rate {Rr}'
    return card
def GetMatchStatus1(match):
    mStatus = match['status']
    return mStatus

def GetLastInning(overs):
    if 'miniscore' not in overs:
        return None
    
    miniscore=overs['miniscore']
    
    
    if 'inningsScores' not in miniscore:
        return None
    
    inningsScores = miniscore['inningsScores']
    
    linningsScores = len(inningsScores)
    if linningsScores <= 0 :
        return None
    
    lastinningsScores=inningsScores[linningsScores-1]
    
    if 'inningsScore' not in lastinningsScores:
        return None
    
    inningsScore = lastinningsScores['inningsScore']
    
    linningsScore = len(inningsScore)
    if linningsScore <= 0 :
        return None
    
    lastinningsScore=inningsScore[linningsScore-1]
    
    return lastinningsScore

def EmptyScoreCard():
    return 'Team 0/0  (0 Ov)'
def GetScorecard(overs):
    lastInning = GetLastInning(overs)
    if lastInning is None:
        return EmptyScoreCard();
    
    
    runs=lastInning['runs']
    wickets=lastInning['wickets']
    overs=lastInning['overs']
    batTeamShortName = lastInning['batTeamShortName']
    card = f'{batTeamShortName} {runs}/{wickets}  ({overs} Ov)'
    return card
def GetRunrate(overs):
    if 'miniscore' not in overs:
        return 'Current Run Rate 0'
    miniscore=overs['miniscore']
    if 'crr' not in miniscore:
        'Current Run Rate 0'
    crr = miniscore['crr']
    card = f'Current Run Rate {crr}'
    return card
def GetMatchStatus(overs):
    if 'miniscore' not in overs:
        return ''
    miniscore=overs['miniscore']
    
    if 'custStatus' not in miniscore:
        return ''
    
    custStatus = miniscore['custStatus']
    
    return custStatus

def GetBowlerStat(bowler):

    name = 'bowler'
    score='0'
    Overs='0'
    wickets='0'
    economy='0'
    
    if bowler is None:
        return f'{name} \n{score}/{wickets} \n({Overs} ov)\n economy {economy}'
    
    if 'name' in bowler:
        name = bowler['name']
    if 'runs' in bowler:
        score = bowler['runs']
    
    if 'overs' in bowler:
        Overs = bowler['overs']
    
    if 'wickets' in bowler:
        wickets = bowler['wickets']
    
    if 'economy' in bowler:
        economy = bowler['economy']
        
    # Economy = bowler['Er']
    card = f'{name} \n{score}/{wickets} \n({Overs} ov)\n economy {economy}'
    return card

def GetBowlerNumber(match,number):
    if match is None:
        return GetBowlerStat(None)
    scorecard = GetLastScorecard(match)
    if 'bowler' not in scorecard:
        return GetBowlerStat(None)
    bowlers = scorecard['bowler']
    if len(bowlers) > number:
        return GetBowlerStat(bowlers[number])
    else:
        return GetBowlerStat(None)
    
        
def GetLastBowler(overs,match=None):
    if 'miniscore' not in overs:
        return GetBowlerNumber(match,0)
    
    miniscore =overs['miniscore']
    
    if 'bowlerStriker' not in miniscore:
        return GetBowlerNumber(match,0)
    
    bowlerStriker = miniscore['bowlerStriker']
    return GetBowlerStat(bowlerStriker)
def GetSecondLastBowler(overs,match=None):

    if 'miniscore' not in overs:
        return GetBowlerNumber(match,1)
    
    miniscore =overs['miniscore']
    
    if 'bowlerNonStriker' not in miniscore:
        return GetBowlerNumber(match,1)
    
    bowlerNonStriker = miniscore['bowlerNonStriker']
    return GetBowlerStat(bowlerNonStriker)
def GetBatsmanStat(batsman):
    name = 'batter'
    runs = 0
    balls = 0
    strkRate=0
    fours = 0
    sixes = 0
    if batsman is None:
        return  f'{name} \n{runs}/{balls} 4({fours}) 6({sixes}) \n sr({strkRate})'
    
    if 'name' in batsman:
        name = batsman['name']
    
    if 'runs' in batsman:
        runs = batsman['runs']
        
    if 'balls' in batsman:
        balls = batsman['balls']
        
    if 'strkRate' in batsman:
        strkRate = batsman['strkRate']
    
    if 'fours' in batsman:
        fours = batsman['fours']
    
    if 'sixes' in batsman:
        sixes = batsman['sixes']
    
    card = f'{name} \n{runs}/{balls} sr({strkRate})\n4({fours}) 6({sixes})'
    return card
def GetBatsmanNumber(match,number):
    if match is None:
        return GetBowlerStat(None)
    scorecard = GetLastScorecard(match)
    if 'batsman' not in scorecard:
        return GetBowlerStat(None)
    batsman = scorecard['batsman']
    if len(batsman) > number:
        return GetBatsmanStat(batsman[number])
    else:
        return GetBatsmanStat(None)
    
def GetBatsman1(overs,match=None):
    if 'miniscore' not in overs:
        return GetBatsmanNumber(match,0)
    
    miniscore =overs['miniscore']
    
    if 'batsmanStriker' not in miniscore:
        return GetBatsmanNumber(match,0)
    
    batsmanStriker = miniscore['batsmanStriker']
    return GetBatsmanStat(batsmanStriker)
def GetBatsman2(overs,match=None):

    if 'miniscore' not in overs:
        return GetBatsmanNumber(match,0)
    
    miniscore =overs['miniscore']
    
    if 'batsmanNonStriker' not in miniscore:
        return GetBatsmanNumber(match,0)
    
    batsmanNonStriker = miniscore['batsmanNonStriker']
    return GetBatsmanStat(batsmanNonStriker)
def GetProgress(overs):
    if 'miniscore' in overs:
        miniscore = overs['miniscore']
        if 'performance' in miniscore:
            performance = miniscore['performance']
            if len(performance) > 0:
                perform1 = performance[0]
                label = perform1['label']
                runs = perform1['runs']
                return f'{label} : {runs} runs'
    return None
def GetLastBall(overs):
    progress = GetProgress(overs)
    if progress is not None:
        return progress
    else:
        if 'matchHeaders' in overs:
            matchHeaders = overs['matchHeaders']
            if 'state' in matchHeaders:
                state = matchHeaders['state']
                return state
        return ''    
def LastOutBatsman(overs):
    if 'miniscore' in overs:
        miniscore = overs['miniscore']
        if 'partnership' in miniscore:
            partnership = miniscore['partnership']
            return partnership
    return ''

    
            
    

