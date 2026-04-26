import requests
import plotly.express as px
import plotly.graph_objects as go
import statistics as st
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import messagebox

#add comments and maybe next add a back button, and show a list of valid languages, etc
#other possible next steps: give multiple options like most forked, most starred, etc
#creates the root object
def create_ui():
    root = tk.Tk()
    root.title("Input language")
    #gets measurements such of screen width and height to style the widget accordingly
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    scaled_widget_height = int(screen_height / 4)
    scaled_widget_width = int(screen_width / 4)
    screen_middle_width = (screen_width - scaled_widget_width) // 2
    screen_middle_height = (screen_height - scaled_widget_height) // 2
    #ensures the root is sized appropriately
    root.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")

    #creates the frame to add a label and input box on
    #attaches the frame to the root
    frame = tk.Frame(root)
    #creates the label with 10 px of vertical padding
    tk.Label(frame, text = "Language").pack(pady = 10)
    #places the frame at the very center of the root
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")
    #adds the entry to the frame, with 10 px of vertical padding
    entryOne = tk.Entry(frame)
    entryOne.pack(pady = 10)
    #focuses on the entry on start
    entryOne.focus()

#creates a variable which automatically sets the target_language to none,
#because the get_language() function does not return anything
#get_languages doesn't return because it's a command 
    def get_language():
        #creates global target_language so the value can be stored in that variable
        global target_language
        #recieves the value upon clicking submit, capitalizing the first letter and stripping any possible whitespace
        target_language = entryOne.get().strip().title()
        #destroys the root so it doesn't interfere anymore
        root.destroy()

#creates the button
    tk.Button(frame, text = "Submit", command = get_language).pack(pady = 10)
    root.mainloop()
    return target_language

def translation(target_language):
    #loop which checks the code and language within languages.items()
    #if there is a match with the target language it returns the target_code
    #creates a dictionary of the country and codes of the google_translator
    google_translator_dictionary = GoogleTranslator().get_supported_languages(as_dict=True)
    #default boolean (language is not found)
    languageFound = False
    #default target code is english
    target_code = "en"
    #loops over the language and code in the items of dictionary
    for language, code in google_translator_dictionary.items():
        #checks if the submitted language matches any languages in the dictionary
        if target_language == language.title():
            #if it matches, sets the target_code equal to code
            target_code = code
            #sets languageFound as true
            languageFound = True
            #shows a messagebox with info
            messagebox.showinfo("Message", f"Descriptions will be translated to {target_language}!")
            #breaks the loop so it won't search anymore
            break
    #if the language is not found
    if not languageFound:
        #shows that there is an invalid language, and uses english as default
        messagebox.showwarning("Invalid Language", "Invalid language, English will be used as default")
    #messagebox to show a disclaimer because there is delay
    messagebox.showinfo("Delay", "*Disclaimer* \nThere will be some delay for translations!")
    return target_code
def api_call():
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
    return repo_dicts

def populate_dicts(target_code, repo_dicts):
    #process repository information
    #three lists that store the names, number of stars, and hover_texts
    repo_links, stars, hover_texts = [], [], []
    translator = GoogleTranslator(source = "auto", target = target_code)
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
        description = repo_dict["description"] or "No Description"
        try:
            description = translator.translate(repo_dict["description"])
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
    return total_stars, total_repos, repo_links, hover_texts, stars

def get_average_stars(total_stars, total_repos):
    average_stars = total_stars / total_repos
    return average_stars

def get_median_stars(stars):    
    median_stars = st.median(stars)
    return median_stars

def create_graph(repo_links, stars, hover_texts, average_stars, median_stars):
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
            #formats the average stars value
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

target_language = create_ui()
target_code = translation(target_language)
repo_dicts = api_call()
populated_dicts = populate_dicts(target_code, repo_dicts)
average_stars = get_average_stars(populated_dicts[0], populated_dicts[1])
median_stars = get_median_stars(populated_dicts[4])
create_graph(populate_dicts[2], populated_dicts[3], average_stars, median_stars)