class CrowdTangle:
    
    def __init__(self, token):
        self.token = token
        
    def getPosts(self, listIds = '', count = 100, types = '', startDate = '', endDate = '', sortBy = 'overperforming', searchTerm = '', includeHistory = '', language = '', minInteractions = 0, pageAdminTopCountry = '', verified = 'no_filter', brandedContent = 'no_filter', offset = 0):
        
        if count > 100:
            apiCount = 100
        else: 
            apiCount = count
        
        
        postsParams = {
            'token': self.token,
            'listIds': listIds,
            'count': apiCount,
            'types': types,
            'startDate': startDate,
            'endDate': endDate,
            'sortBy': sortBy,
            'searchTerm': searchTerm,
            'includeHistory': includeHistory,
            'language': language,
            'minInteractions': minInteractions,
            'pageAdminTopCountry': pageAdminTopCountry,
            'verified': verified,
            'brandedContent': brandedContent,
            'offset': 0
            }
        
        result = []
        innerParams = {}

        data = rq.get('https://api.crowdtangle.com/posts', params = postsParams).json()
        
        if data['status'] != 200: 
                print(data['message'])
        result = data
        
        if count > 100:
            time.sleep(11)

        while data['result']['pagination'] and len(result['result']['posts']) < count: 

                innerParams = postsParams
                innerParams['endDate'] = str(datetime.strptime(data['result']['posts'][99]['date'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds = -1))
                data = rq.get('https://api.crowdtangle.com/posts', innerParams).json()
                if data['status'] != 200: 
                    print(data['message'])
                result['result']['posts'] = result['result']['posts'] + data['result']['posts']
                time.sleep(11)
    
        df = pd.DataFrame(result['result']['posts'])
        df.set_index('platformId')
        expandedLinks = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['expandedLinks'])])[0].to_dict()).transpose()
        statisticsActual = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['actual'].apply(pd.Series))
        statisticsExpected = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['expected'].apply(pd.Series))
        statisticsActual.columns = ["actual" + x for x in list(statisticsActual.columns)]
        statisticsExpected.columns = ["expected" + x for x in list(statisticsExpected.columns)]
        account = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['account'])]))
        media = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['media'])])[0].to_dict()).transpose()
        media.columns = ["media" + x for x in list(media.columns)]
        
        df = df.drop(['expandedLinks','statistics','account','media'], axis = 1)
        df = pd.concat([df, expandedLinks, statisticsActual, statisticsExpected, account, media], axis = 1)
        
        return df
    
    def getPost(self, id = '', ctId = False, includeHistory = '', account = ''):
        
        result = []
        if ctId == False:
            
            postParams = {
            'token': self.token,
            'includeHistory': '',
            'account': ''
            }

            data = rq.get('https://api.crowdtangle.com/post/' + id, params = postParams).json()
            
            df = pd.DataFrame(data['result']['posts'])
            df.set_index('platformId')
            expandedLinks = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['expandedLinks'])])[0].to_dict()).transpose()
            statisticsActual = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['actual'].apply(pd.Series))
            statisticsExpected = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['expected'].apply(pd.Series))
            statisticsActual.columns = ["actual" + x for x in list(statisticsActual.columns)]
            statisticsExpected.columns = ["expected" + x for x in list(statisticsExpected.columns)]
            account = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['account'])]))
            media = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['media'])])[0].to_dict()).transpose()
            media.columns = ["media" + x for x in list(media.columns)]

            df = df.drop(['expandedLinks','statistics','account','media'], axis = 1)
            result = pd.concat([df, expandedLinks, statisticsActual, statisticsExpected, account, media], axis = 1)
            
        
        if ctId == True:
            
            postParams = {
            'token': 'szLzo70Wce3nglKhkv09heg1vZN82lz6VfYijd0C',
            'includeHistory': '',
            'account': ''
            }

            data = rq.get('https://api.crowdtangle.com/ctpost/' + id, params = postParams).json()
            
            df = pd.DataFrame(data['result']['posts'])
            df.set_index('platformId')
            expandedLinks = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['expandedLinks'])])[0].to_dict()).transpose()
            statisticsActual = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['actual'].apply(pd.Series))
            statisticsExpected = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['expected'].apply(pd.Series))
            statisticsActual.columns = ["actual" + x for x in list(statisticsActual.columns)]
            statisticsExpected.columns = ["expected" + x for x in list(statisticsExpected.columns)]
            account = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['account'])]))
            media = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['media'])])[0].to_dict()).transpose()
            media.columns = ["media" + x for x in list(media.columns)]

            df = df.drop(['expandedLinks','statistics','account','media'], axis = 1)
            result = pd.concat([df, expandedLinks, statisticsActual, statisticsExpected, account, media], axis = 1)
            
        return result
        
    def getLinks(self, link = '', count = 100, types = '', startDate = '', endDate = '', sortBy = 'overperforming', includeHistory = '', includeSummary = '', platforms = '', searchField = '', offset = 0):
        
        linksParams = {
            'token':self.token,
            'link': link,
            'count': count,
            'startDate': startDate,
            'endDate': endDate,
            'sortBy': sortBy,
            'includeHistory': includeHistory,
            'includeSummary': includeSummary,
            'platforms': platforms,
            'searchField': searchField,
            'offset': offset
            }
        
        result = []
        innerParams = {}
        runningOffset = linkParams['offset']

        data = rq.get('https://api.crowdtangle.com/links', params = linksParams).json()
        result = data
        
        if count > 500:
            time.sleep(11)

        while data['result']['pagination'] and len(result['result']['posts']) < count: 

#                 innerParams = postParams
#                 innerParams['endDate'] = str(datetime.strptime(data['result']['posts'][99]['date'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds = -1))
            data = rq.get(data['result']['pagination']).json()
            result['result']['posts'] = result['result']['posts'] + data['result']['posts']
            time.sleep(11)
            runningOffset += 100
            if runningOffset % 1000 == 0:
                linkParams['offset'] = runningOffset
                data = rq.get('https://api.crowdtangle.com/links', params = linkParams).json()
    
        df = pd.DataFrame(result['result']['posts'])
        df.set_index('platformId')
        expandedLinks = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['expandedLinks'])])[0].to_dict()).transpose()
        statisticsActual = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['actual'].apply(pd.Series))
        statisticsExpected = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['statistics'])])['expected'].apply(pd.Series))
        statisticsActual.columns = ["actual" + x for x in list(statisticsActual.columns)]
        statisticsExpected.columns = ["expected" + x for x in list(statisticsExpected.columns)]
        account = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['account'])]))
        media = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else [np.nan,np.nan] for x in list(df['media'])])[0].to_dict()).transpose()
        media.columns = ["media" + x for x in list(media.columns)]
        
        df = df.drop(['expandedLinks','statistics','account','media'], axis = 1)
        df = pd.concat([df, expandedLinks, statisticsActual, statisticsExpected, account, media], axis = 1)
        
        return df
    
    def getLists(self):
    
        linkParams = {
        'token':self.token
        }
        
        data = rq.get('https://api.crowdtangle.com/lists', params = linkParams).json()
        
        return pd.DataFrame(data['result']['lists'])
    
    
    def getLeaderboard(self):
        
        leaderdata = rq.get('https://api.crowdtangle.com/leaderboard', params = linkParams).json()
        df = pd.DataFrame(leaderdata['result']['accountStatistics'])

        account = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['account'])]))

        summary = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['summary'])]))
        summary.columns = ["summary" + "_" + x for x in list(summary.columns)]

        breakdown = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['breakdown'])]))

        subscriber = pd.DataFrame(pd.DataFrame([x if type(x) != np.float else np.nan for x in list(df['subscriberData'])]))

        typesDf = pd.DataFrame()

        for key in set(breakdown):
            temp = pd.DataFrame(pd.DataFrame([x if type(x) != float else {} for x in list(breakdown[str(key)])]))
            temp.columns = [str(key) + "_" + x for x in list(temp.columns)]
            typesDf = pd.concat([typesDf, temp], axis = 1)

        result = pd.concat([account, summary, typesDf, subscriber], axis = 1)

        return result