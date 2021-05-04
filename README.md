# PyTangle

![py_ct_logo](https://user-images.githubusercontent.com/48947001/116953965-9fa08d00-ac5c-11eb-9c12-ba82c72ccc8d.png)


Python wrapper for the Crowdtangle API that returns the results as a pandas dataframe. While this package will eventually be published to PyPl, this repository is public and the package can be installed using the code in the block below. 

## Installing PyTangle

```
pip install git+git://github.com/michaelscholtens/PyTangle.git

# If you are using a notebook, preceed the pip install with an '!' to run the line as if you were in Command Prompt or Terminal.
# !pip install git+git://github.com/michaelscholtens/PyTangle.git

import PyTangle as pt
```

## Getting Started

PyTangle works by creating a PyTangle object that accepts your desired CrowdTangle token, which allows you to call functions that abstract the Crowdtangle endpoints and returns the results as pandas dataframes for ease of use and quick analysis. 

To create a PyTangle object, you call the function PyTangle() and pass your desired token as the only argument. 
```
py_t = pt.PyTangle({Your Crowdtangle API Token})
```
Currently, a PyTangle object has two attributes, token and log. The token attribute is the token passed as the argument when the object is created. While the log attribute is used to maintain an error log for the provided functions that can be incorporated into larger applications that rely on this package. 

In the future PyTangle objects may have more attributes to accomodate new functions or uses for this package.

## Functions 

With a PyTangle object you may call one of six functions. 

* getLists()
* getPost()
* getPosts()
* getLinks()
* getLeaderboard()
* crowdtangleExport()

### getLists()

The getLists() function returns a dataframe of lists in the dashboard associated with the supplied API token. 

This function does not take an arguement, as the token is supplied by the PyTangle object. 
```
py_t.getLists()
```

### getPost(id = '', includeHistory = 'False', account = '')

The getPost() functions wraps the /post/:id endpoint allowing you to search for a specific post by crowdtangle ID number and returns a dataframe with the desired post. The endpoint documentation can be found [here](https://github.com/CrowdTangle/API/wiki/Posts#get-postid).

The function accepts the following arguments:
| Argument      | Datatype      | Description  | Default Value |
| :------------- |:-------------| :-----|:---|
| id      | str | Crowdtangle ID number | N/A |
| includeHistory     | str      | Includes timestep data for growth of each post returned.   | 'False' |
| account | str      |   Slug or ID of the posting account. This field is only necessary for reddit | N/A |

```
py_t.getPost(id = 47657117525_10154014482272526, includeHistory = 'True')
```

### getPosts(listIds = '', count = 100, types = '', startDate = '', endDate = '', sortBy = 'overperforming', searchTerm = '', includeHistory = '', language = '', minInteractions = 0, pageAdminTopCountry = '', verified = 'no_filter', brandedContent = 'no_filter', offset = 0)

The getPosts() functions wraps the /posts endpoint allowing you to search for posts by crowdtangle list ID and returns a dataframe of the results. The endpoint documentation can be found [here](https://github.com/CrowdTangle/API/wiki/Posts).

The function accepts the following arguments:
| Argument      | Datatype      | Description  | Default Value |
| :------------- |:-------------| :-----|:---|
| listIds      | str | Crowdtangle list IDs from which to pull posts. Include multiple list by separating each id with a comma. | null (returns posts from all lists in the Crowdtangle Dashboard) |
| count     | int      | Number of posts to return. If the 'sortBy' parameter is not 'date', this number is limited to 10000 posts.   | 100 |
| types | str   | Limited the types of posts returned. Options include: album, igtv, link, live_video, live_video_complete, live_video_scheduled, native_video, photo, status, video, vine, youtube | null (all) |
| startDate | str | The earliest date at which a post could be posted. Time zone is UTC. Format is “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd” | Most recent posts given the other search criteria | 
| endDate | str | The latest date at which a post could be posted. Time zone is UTC. Format is “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd”. | present | 
| sortBy | str | The method by which to filter and order posts. Options include: date, interaction_rate, overperforming, total_interactions, underperforming. | 'overperforming'|
|searchTerm | str | Returns only posts that match this search term. Terms AND automatically. Separate with commas for OR, use quotes for phrases. E.g. CrowdTangle API -> AND. CrowdTangle, API -> OR. "CrowdTangle API" -> AND in that exact order. You can also use traditional Boolean search with this parameter. | null | 
| includeHistory | str | Includes timestep data for growth of each post returned. | 'False' |
| language | str | [Two letter locale code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) | null |
| minInteractions | int | Exclude posts with total interactions below this threshold. | 0 | 
| pageAdminTopCountry | str |  [Two letter locale code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) | null | 
| verified | str | Limits to posts where the account has the verified setting matching the input. Options include: only, exclude, no_filter. | 'no_filter' |
| brandedContent | str | Limits to or excludes posts that have been marked as Branded Content, either as Publisher or Marketer. Options include: as_publisher, as_marketer, exclude, no_filter | no_filter | 
| offset | int | The number of posts to offset | 0 |

```
py_t.getPosts(listIds = '1234567', count = 100, startDate = '2020-01-01', endDate = '2020-12-31', sortBy = 'date')
```

### getLinks(link = '', count = 100, startDate = '', endDate = '', sortBy = 'date', includeHistory = '', includeSummary = '', platforms = '', searchField = '', offset = 0)

The getLinks() functions wraps the /links endpoint allowing you to search for posts by crowdtangle the link shared and returns a dataframe of the results. The endpoint documentation can be found [here](https://github.com/CrowdTangle/API/wiki/Links).

The function accepts the following arguments:
| Argument      | Datatype      | Description  | Default Value |
| :------------- |:-------------| :-----|:---|
| link      | str | Link to search by. Links often work better as a url without the preceeding 'http(s)://' | Required |
| count     | int      | Number of posts to return. If the 'sortBy' parameter is not 'date', this number is limited to 1000 posts.  | 100 |
| startDate | str | The earliest date at which a post could be posted. Time zone is UTC. Format is “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd” | Most recent posts given the other search criteria | 
| endDate | str | The latest date at which a post could be posted. Time zone is UTC. Format is “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd”. | present | 
| sortBy | str | The method by which to filter and order posts. Options include: date, interaction_rate, overperforming, total_interactions, underperforming. | 'date'|
| includeHistory | str | Includes timestep data for growth of each post returned. | 'False' |
| includeSummary | str | Adds a "summary" section with AccountStatistics for each platform that has posted this link. It will look beyond the count requested to summarize across the time searched. Requires a value for startDate. | 'False' |
| platforms | str | The platforms from which to retrieve links. This value can be comma-separated. Options include: facebook, instagram, reddit. | null (all) |
| searchField | str | Allows you to search URLs containing query strings. Options include: Include_query_strings | null | 
| offset | int | The number of posts to offset | 0 |

```
py_t.getLinks(link = 'github.com', count = 1000, sortBy = 'date')
```

### getLeaderboard(listId = '')

The getLinks() functions wraps the /leaderboard endpoint allowing you to retrieve the leaderboard data for a given Crowdtangle list and returns a dataframe of the results. The endpoint documentation can be found [here](https://github.com/CrowdTangle/API/wiki/Leaderboard).

The function accepts the following arguments:
| Argument      | Datatype      | Description  | Default Value |
| :------------- |:-------------| :-----|:---|
| listId      | str | The list of the leaderboard to retrieve. | Entire Dashboard |

```
py_t.getLeaderboard(listId = '1234567')
```

### crowdtangleExport(links, groupListName = 'tangle_groups', pageListName = 'tangle_page", filePath = '')

The crowdtangleExport() function ingests a list of urls of facebook groups and/or pages, and exports a csv file in the correct format to use the batch upload fuction through the Crowdtangle GUI. 


The function accepts the following arguments:
| Argument      | Datatype      | Description  | Default Value |
| :------------- |:-------------| :-----|:---|
| links      | list of strs | The links must be in the form of a list of strings, with each string being a url for a Facebook group or page. | Required |
| groupListName | str | This is the name of the Crowdtangle list to which you would like to upload all Facebook groups in the links list. | 'tangle_groups' |
| pageListName | str | This is the name of the Crowdtangle list to which you would like to upload all Facebook pages in the links list. | 'tangle_pages' |
| filePath | str | This is the location to which you would like to write the csv file that is ready for batch upload. | null (current directory) | 

```
py_t.crowdtangleExport(links, groupListName = 'tangle_groups', pageListName = 'tangle_page")
```
