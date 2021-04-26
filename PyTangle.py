#Dependencies
import pandas as pd
import numpy as np
import requests as rq
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta

#This class is used to interact with the Crowdtangle API.
class PyTangle:
    
    #When initiating a PyTangle object, you must set the token from the appropriate dashboard. This is particularily important for getPosts, getists, and getLeaderboard functions.
    def __init__(self, token):
        self.token = token
        self.log = logging.getLogger(__name__)
        logging.captureWarnings(True)
        
    #The getPosts function returns a Pandas dataframe of posts from one of the lists found in you Crowdtangle Dashboard.
    def getPosts(self, listIds = '', count = 100, types = '', startDate = '', endDate = '', sortBy = 'overperforming', searchTerm = '', includeHistory = '', language = '', minInteractions = 0, pageAdminTopCountry = '', verified = 'no_filter', brandedContent = 'no_filter', offset = 0):
        
        #Each request to the Crowdtangle API is limited to 100, so we reset the count parameter for each new call until the count desired count is reached.
        if count > 100:
            apiCount = 100
        else: 
            apiCount = count
        
        #API parameters are passed as a dictionary.
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
        
        #The maximum batch size within Crowdtangle is 10000.
        if count > 10000: 
            self.log.warning('Posts returned limited to 10000 with a sortBy parameter of' + postsParams['sortBy'] +". If you would like to return more than 10000 posts, sortBy 'date'")
            postsParams['count'] = 10000
                    
        data = rq.get('https://api.crowdtangle.com/posts', params = postsParams).json()
        
        #If the call is not sucessful the script will log the response message and raise an error.
        if data['status'] != 200: 
            self.log.error(data['message'])
            raise Exception('Crowdtangle API call has failed.')
                
        result = data
        
        #If the count parameter is high enough this condition check makes sure there is not a call rate-limit error.
        if count > 100:
            time.sleep(11)
        
        #If the sortBy parameter is 'date', then this code block allows for the appropriate pagination. 
        if(postsParams['sortBy'] == 'date'):
        
            while 'nextPage' in data['result']['pagination'] and 0 < len(result['result']['posts']) < count: 
                
                #Parameters are passed from the first call to the second. 
                
                innerParams = postsParams
                
                #The 'endDate' parameter is adjusted to collect the next 100 posts.
                
                innerParams['endDate'] = str(datetime.strptime(data['result']['posts'][99]['date'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds = -1))
                data = rq.get('https://api.crowdtangle.com/posts', innerParams).json()
                
                #If the call is not sucessful the script will log the response message and raise an error.
                if data['status'] != 200: 
                    self.log.error(data['message'])
                    raise Exception('Crowdtangle API call has failed.')
                
                #The output of the API call is then appended to the results object created with the first call. 
                result['result']['posts'] = result['result']['posts'] + data['result']['posts']
                time.sleep(11)
            
        #If the sortBy parameter is not 'date', then standard pagination is employed.
        if(postsParams['sortBy'] != 'date'):
        
            while 'nextPage' in data['result']['pagination'] and 0 < len(result['result']['posts']) < count: 

                data = rq.get(data['result']['pagination']['nextPage']).json()
                
                #If the call is not sucessful the script will log the response message and raise an error.
                if data['status'] != 200: 
                    self.log.error(data['message'])
                    raise Exception('Crowdtangle API call has failed.')
                    
                result['result']['posts'] = result['result']['posts'] + data['result']['posts']
                time.sleep(11)
        
        #After the API calls are completed, the posts are converted into a Pandas Dataframe.
        df = pd.DataFrame(result['result']['posts'])
        
        #In the event that the Crowdtangle API call was successful but there were no results, this line ensures that the script will not try to unpack non-existent JSON fields.
        if len(df) != 0:
            df.set_index('platformId')
        
        #These lines a not intuitive at all but unpacks columns that store dictionaries into new columns. There may be more intuitive ways to do this and this section is a priority for refactoring.
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
        
        else:
            #In the event that the API call did not return any posts, this line logs the event along with the parameters for the call, so the call can be replicated to determine if the result is a mistake.
            self.log.warning('No posts were returned with call' + str(postsParams))
    
    #The getPost function will return the details of a single post. The post is located using the id number.
    def getPost(self, id = '', includeHistory = '', account = ''):
        
        result = []

        #API parameters are passed as a dictionary.
        postParams = {
        'token': self.token,
        'includeHistory': '',
        'account': ''
        }

        data = rq.get('https://api.crowdtangle.com/post/' + id, params = postParams).json()

        #If the call is not sucessful the script will log the response message and raise an error
        if data['status'] != 200: 
            self.log.error(data['message'])
            raise Exception('Crowdtangle API call has failed.')
                             
        #After the API calls are completed, the posts are converted into a Pandas Dataframe.
        df = pd.DataFrame(data['result']['posts'])
                             
        #In the event that the Crowdtangle API call was successful but there were no results, this line ensures that the script will not try to unpack non-existent JSON fields.
        if len(df) != 0:

            df.set_index('platformId')

            #These lines a not intuitive at all but unpack columns that store dictionaries into new columns. There may be more intuitive ways to do this and this section is a priority for refactoring.
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

        else:
            #In the event that the API call did not return any posts, this line logs the event along with the parameters for the call, so the call can be replicated to determine if the result is a mistake.
            self.log.warning('No post was returned with call' + str(postParams))
    
    #This function returns posts that share a given link. 
    def getLinks(self, link = '', count = 100, startDate = '', endDate = '', sortBy = 'date', includeHistory = '', includeSummary = '', platforms = '', searchField = '', offset = 0):
        
        #API parameters are passed as a dictionary.
        if count > 1000:
            apiCount = 1000
        else: 
            apiCount = count
        
        linksParams = {
            'token':self.token,
            'link': link,
            'count': apiCount,
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
        
        # The links endpoint is limited to 1000 posts. This logic check ensures that this limitation is respected. A warning will be logged about the event.                  
        if count > 1000 and linksParams['sortBy'] != 'date': 
            self.log.warning('Posts returned limited to 1000 with a sortBy parameter of' + linksParams['sortBy'] +". If you would like to return more than 1000 posts, sortBy 'date'")
            linksParams['count'] = 1000
                 
        data = rq.get('https://api.crowdtangle.com/links', params = linksParams).json()
        
        #If the call is not sucessful the script will log the response message and raise an error
        if data['status'] != 200: 
            self.log.error(data['message'])
            raise Exception('Crowdtangle API call has failed.')
            
        result = data
        
        #If the count parameter is high enough this condition check makes sure there is not a call rate-limit error.
        if count > 1000:
            time.sleep(31)
        
        #If the sortBy parameter is not 'date', then standard pagination is employed.
        if(linksParams['sortBy'] == 'date'):
        
            while 'nextPage' in data['result']['pagination'] and len(result['result']['posts']) < count: 

                innerParams = linksParams
                innerParams['endDate'] = str(datetime.strptime(data['result']['posts'][99]['date'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds = -1))
                data = rq.get('https://api.crowdtangle.com/links', innerParams).json()
                
                #If the call is not sucessful the script will log the response message and raise an error
                if data['status'] != 200: 
                    self.log.error(data['message'])
                    raise Exception('Crowdtangle API call has failed.')
                
                result['result']['posts'] = result['result']['posts'] + data['result']['posts']
                time.sleep(31)
                             
        #After the API calls are completed, the posts are converted into a Pandas Dataframe.
        df = pd.DataFrame(result['result']['posts'])
        
        #In the event that the Crowdtangle API call was successful but there were no results, this line ensures that the script will not try to unpack non-existent JSON fields.
        if len(df) != 0:
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

        else:
            #In the event that the API call did not return any posts, this line logs the event along with the parameters for the call, so the call can be replicated to determine if the result is a mistake.
            self.log.error('No posts were returned with call' + str(linksParams))
    
    #This function returns all lists associated with a Crowdtangle API token.
    def getLists(self):
                             
        #API parameters are passed as a dictionary.
        linkParams = {
        'token':self.token
        }
        
        data = rq.get('https://api.crowdtangle.com/lists', params = linkParams).json()
        
        #If the call is not sucessful the script will log the response message and raise an error
        if data['status'] != 200: 
            self.log.error(data['message'])
            raise Exception('Crowdtangle API call has failed.')
                                 
        return pd.DataFrame(data['result']['lists'])
    
    #This function returns the leaderboard data for a Crowdtangle list.
    def getLeaderboard(self, listId = ''):
        
        #API parameters are passed as a dictionary.
        linkParams = {
        'token':self.token,
        'listId': listId
        }
        
        leaderdata = rq.get('https://api.crowdtangle.com/leaderboard', params = linkParams).json()
        
        #If the call is not sucessful the script will log the response message and raise an error
        if leaderdata['status'] != 200: 
            self.log.error(leaderdata['message'])
            raise Exception('Crowdtangle API call has failed.')
                                 
        df = pd.DataFrame(leaderdata['result']['accountStatistics'])

        #The following lines unpack JSON data into individual columns.
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
    
    #This function takes a list of links and exports a file in the format for bulk upload to Crowdtangle.
    def crowdtangleExport(self, links, listName = 'tangle', filePath = ''):
        df = pd.DataFrame(links, columns=['Page or Account URL'])
        df["List"] = [listName + "_groups" if "group" in row else listName + "_pages" for row in df['Page or Account URL']]
        if filePath:
            df.to_csv(filePath + 'CtExport' + time.strftime("%d_%h_%y_%H_%M", time.localtime()) + '.csv', index = False)
        else:
            df.to_csv('CtExport' + time.strftime("%d_%h_%y_%H_%M", time.localtime()) + '.csv', index = False)
        return df
