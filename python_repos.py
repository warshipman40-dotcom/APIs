import requests
import plotly.express as px
import plotly.graph_objects as go
#make an API call
#assigns the URL of the API call to the variable
url = "https://api.github.com/search/repositories"
#query string (sorts only language python and repositories with over 10,000 stars)
url += "?q=language:python+sort:stars+stars:>10000"
#we make sure our header for the API call uses v3 of the API
#returns results in the JSON format
headers = {"Accept" : "application/vnd.github.v3+json"}
#requests makes the call to the API through get()
#we pass the URL and header we defined 
#we assign the response object to variable r
r = requests.get(url, headers = headers)
#response object has an attribute called status code
#status code of 200 indicates success
print(f"Status code: {r.status_code}")
#since it is in json format, we use the json() method to convert to a python object
response_dict = r.json()
#prints the keys which gives us the contents
print(response_dict.keys())

print(f"Total Repositories: {response_dict["total_count"]}")
print(f"Complete results : {not response_dict["incomplete_results"]}")

#explore information about the repositories
#the value associated with items is a list containing a number of dictionaries
#each dictionary contains data about a repository
repo_dicts = response_dict["items"]
#we print this to see how many repositories we have info for
print(f"Repositories returned: {len(repo_dicts)}")

#examines the first repository
#repo_dict = repo_dicts[0]
#prints the number of keys to see how much information we have
#print(f"\nKeys: {len(repo_dict)}")
#prints each individual key to see what kind of information is included
#for key in sorted(repo_dict.keys()):
    #print(key)

# print("\nSelected information about repository one")
# for repo_dict in repo_dicts:
#     print(f"Name: {repo_dict["name"]}")
#     #we use the key owner to access the dictionary representing the owner
#     #then we use the key dictionary to access the login name
#     print(f"Owner: {repo_dict["owner"]["login"]}")
#     #we access the number of stars the project has earned
#     print(f"Stars : {repo_dict["stargazers_count"]}")
#     #we get the creation date
#     print(f"Created: {repo_dict["created_at"]}")
#     #we get the updated date
#     print(f"Updated : {repo_dict["updated_at"]}")
#     #we also get the description of the repository
#     print(f"Description : {repo_dict["description"]}")

#process repository information
#three lists that store the names, number of stars, and hover_texts
repo_links, stars, hover_texts = [], [], []
for repo_dict in repo_dicts:
    #adds the information to the lists
    stars.append(repo_dict["stargazers_count"])
    #turn repo names into active links
    repo_name = repo_dict["name"]
    #uses the "html_url" key to get the url
    repo_url = repo_dict["html_url"]
    #we use the html anchor tag to create a hyperlink using href
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    #this link is then appended to the list
    repo_links.append(repo_link)
    #Build hover texts
    #pulls the owner and description from the dictionaries
    owner = repo_dict["owner"]["login"]
    description = repo_dict["description"]
    #plotly allows you to use HTML code within text elements 
    #we use <br /> for a new line
    hover_text = f"{owner} <br /> {description}"
    #this labels is appended to out list
    hover_texts.append(hover_text)

total_stars = sum(stars)
total_repos = len(stars)
average_stars = total_stars / total_repos

#creates a bar graph of the most popular APIS
title = "Most-Starred Python Projects on GitHub"
#labels of the graph
labels = {"x" : "Repository Name", "y" : "Stars"}
#passes in the repository names, the number of stars, and label names
#label names are added to the bars
#hover_name takes in a single string
#passes in repo_links for x so that when a person clicks the project name it sends them to the github link
#hover_name passes in hover_texts so that when the user hovers over the bar, the tooltip is shown
fig = px.bar(x = repo_links, y = stars, title = title, labels = labels, hover_name = hover_texts)
#changes font sizes using update_layout()
fig.update_layout(title_font_size = 28, xaxis_title_font_size = 20, yaxis_title_font_size = 20)
#when we use "paper" as our system, 0 becomes far left edge of the chart while 1 becomes far right edge of chart
fig.add_trace(
    go.Scatter(
        #ensures our x-axis is the same
        x = repo_links, 
        #this gives us a list (each index populated with average_stars) that has the len of the x-axis
        y = [average_stars] * len(repo_links),
        #ensures the line is shown as a line and not markers, etc
        mode = "lines", 
        #gives the label a name
        name = "Average Stars per Repository",
        #creates a black dotted line
        line = dict(color = "black", dash = "dot", ), 
        #on hover, shows average stars %{y} represents the y_values or average stars
        hovertemplate = "Average Stars: %{y}"
    )
)
#traces refers to the collection of data on our graph
#update_traces() takes different arguments
#any argument starting with marker_ affects markers on the chart
#hoverlabel controls the visual style of the tooltip box
#we set the background color of the tooltip box to black
#we set the font_color of the tooltip box to white
fig.update_traces(marker_color = "SteelBlue", marker_opacity = 0.7, 
    hoverlabel = dict(
        bgcolor = "black", 
        font_color = "white"
    ))
fig.show()