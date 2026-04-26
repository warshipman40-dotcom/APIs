import requests
import plotly.express as px
import plotly.graph_objects as go
import statistics as st
from deep_translator import GoogleTranslator
import tkinter as tk
import csv

filename = "languages.csv"
languages = {}
with open(filename) as f:
    reader = csv.reader(f)
    #skips the first line
    for line in range(1):
        next(reader)
    for row in reader:
        language = row[0]
        code = row[1]
        languages[code] = language
        
root = tk.Tk()
root.title("Input language")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
scaled_widget_height = int(screen_height / 4)
scaled_widget_width = int(screen_width / 4)
screen_middle_width = (screen_width - scaled_widget_width) // 2
screen_middle_height = (screen_height - scaled_widget_height) // 2
root.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")

frame = tk.Frame(root)
tk.Label(frame, text = "Language").pack(pady = 10)
frame.place(relx = 0.5, rely = 0.5, anchor = "center")
entryOne = tk.Entry(frame)
entryOne.pack(pady = 10)
entryOne.focus()

target_language = None
def get_language():
    target_language = entryOne.get().strip().title()
    root.destroy()
    return target_language


tk.Button(frame, text = "Submit", command = get_language).pack(pady = 10)
#print(get_language())
root.mainloop()
#possible try to give them the option for the range of repos they want to get
#make an API call
#assigns the URL of the API call to the variable
url = "https://api.github.com/search/repositories"
#query string (sorts only language python and repositories with over 10,000 stars)
url += "?q=language:python+sort:stars+stars:>10000"
#this gives more repositories 
url += "&per_page=50"
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
#print(response_dict.keys())

#print(f"Total Repositories: {response_dict["total_count"]}")
#print(f"Complete results : {not response_dict["incomplete_results"]}")

#explore information about the repositories
#the value associated with items is a list containing a number of dictionaries
#each dictionary contains data about a repository
repo_dicts = response_dict["items"]
#we print this to see how many repositories we have info for
print(f"Repositories returned: {len(repo_dicts)}")
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
    #translates each description
    #try and except because not all descriptions are valid
    try:
        description = GoogleTranslator(source = "auto", target = "en").translate(repo_dict["description"])
    except Exception:
        description = "No Description"
        pass
    #plotly allows you to use HTML code within text elements 
    #we use <br /> for a new line
    hover_text = f"{owner} <br /> {description}"
    #this labels is appended to out list
    hover_texts.append(hover_text)

total_stars = sum(stars)
total_repos = len(stars)
average_stars = total_stars / total_repos
median_stars = st.median(stars)
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
#go.Scatter() will basically create a scatter plot, taking in x and y values
#we can set the mode to lines to ensure that it is displayed as a line
#using go.Scatter() was intentional so features like styling, legend, and hovertemplate were available
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
        hovertemplate = "Average Stars: %{y:,.2f}"
    )
)
fig.add_trace(
    go.Scatter(
        x = repo_links, 
        y = [median_stars] * len(repo_links),
        mode = "lines",
        name = "Median of Stars per Repository",
        line = dict(color = "red", dash = "dot"),
        hovertemplate = "Median Stars : %{y:,.2f}"
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