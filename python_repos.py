import requests
import plotly.express as px
import plotly.graph_objects as go
import statistics as st
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
class RepositoryData:
    """Class that uses Github API to extract data and uses several modules to improve user experience"""
    #AFTER WE FINISH ADDING ALL THE REST OF THE FUNCTIONS / GUI ADD SELF AND CALL THE CLASS FROM DIFFERENT FILE FOR OBJECT ORIENTED PROGRAMMING
    #NEXT PLAN : ADD A BUTTON WHICH GIVES YOU THE TEXT OPTION IF SELECT DOWN DOESN't WORK, OR DO SOMETHING ELSE TO THE TEXT OPTION
    #other possible next steps: give multiple options like most forked, most starred, etc
    #creates the root object
    def create_ui():
        #try making another combobox option that takes different languages, not just python and sees their repos
        #example, using java or javascript, also allowing user to pick the number of stars they want (entrybox for that)
        """Creates the UI using Tkinter"""
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
        #places the frame at the very center of the root
        frame.place(relx = 0.5, rely = 0.5, anchor = "center")
        #creates a label which instructs users to select their language
        ttk.Label(frame, text = "Select your language:", font = ("Arial", 10)).grid(row = 1, column = 1, padx = 5, pady = 10)
        #special tkinter variable which holds a string
        #allows the widget to automatically update when variable changes
        n = tk.StringVar()
        #creates the dropdown menu, so when a user selects a language it display that langauge
        language_chosen = ttk.Combobox(frame, width = 27, textvariable = n)
        #["values"] must be used 
        #stores the list of supported languages and allows them to be displayed
        languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        #converts the dictionary keys to a list
        #converting this dictionary into a list allows tkinter to see each individual string
        #uses list comprehension to capitalize each element within languages_dict.keys() by looping over them
        language_chosen["values"] = list(lang.title() for lang in languages_dict.keys())
        #print(language_chosen["values"])
        #.pack() allows these tkinter items to be displayed on the frame
        language_chosen.grid(row = 1, column = 2)
        language_chosen.set("English")
        m = tk.StringVar()
        ttk.Label(frame, text = "Programming language: ", font = ("Arial", 10)).grid(row = 2, column = 1)
        progamming_language_chosen = ttk.Combobox(frame, width = 27, textvariable = m)
        #stores these values into our combobox widget
        progamming_language_chosen["values"] = ["C", "Python", "Java", "Javascript", "Typescript"]
        progamming_language_chosen.grid(row = 2, column = 2)
        #sets a default programming language (python)
        progamming_language_chosen.current(1)
        #language_chosen.current() can be used with indexes instead
        #for number of stars, set the limitations later
        tk.Label(frame, text = "Number of Stars: ", font = ("Arial", 10)).grid(row = 3, column = 1, pady = 10)
        entry = tk.Entry(frame, width = 30)
        entry.grid(row = 3, column = 2)
        #inserts a default value for the entry
        entry.insert(0, 1000)

    #creates a variable which automatically sets the target_language to none,
    #because the get_language() function does not return anything
    #get_languages doesn't return because it's a command 
        def get_language():
            #creates global variables so that these variables can be access outside of the function
            global target_language
            global num_stars
            global programming_language
            #recieves the value upon clicking submit, capitalizing the first letter and stripping any possible quotes or commas  
            target_language = language_chosen.get().strip("'\",").title()
            programming_language = progamming_language_chosen.get()
            try:
                #has to turn it into int so we can check if its valid
                num_stars = int(entry.get().strip())
            except ValueError:
                messagebox.showwarning("Invalid Literal", "Please insert an integer!")
                #prevents window from closing instead of going to root.destroy()
                entry.delete(0, "end")
                return
            #destroys the root so it doesn't interfere anymore
            root.destroy()
        #closing function that destroys root, sets target_language to None to avoid a error message, and gives a closing message
        def on_close():
            target_language = None
            messagebox.showinfo("Closing", "Closing... ")
            root.destroy()

        #creates the submit button

        tk.Button(frame, text = "Submit", command = get_language).grid(columnspan = 2, row = 4, column = 1, pady = 10)
        #closes window on close instead of automatically going to english
        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()
        return target_language

    def translation(target_language):
        """Translates descriptions using GoogleTranslator"""
        #loop which checks the code and language within languages.items()
        #if there is a match with the target language it returns the target_code
        #creates a dictionary of the country and codes of the google_translator
        google_translator_dictionary = GoogleTranslator().get_supported_languages(as_dict=True)
        #default boolean (language is not found)
        #default target code is english
        target_code = "en"
        languageFound = False
        #loops over the language and code in the items of dictionary
        for language, code in google_translator_dictionary.items():
            #checks if the submitted language matches any languages in the dictionary
            if target_language.lower() == language.lower().strip("'\","):
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
        """Makes an API call to github to retrieve repositories"""
        #possible try to give them the option for the range of repos they want to get
        #make an API call
        #assigns the URL of the API call to the variable
        url = "https://api.github.com/search/repositories"
        #query string (sorts only language python and repositories with over 10,000 stars)
        url += f"?q=language:{programming_language}+sort:stars+stars:>{num_stars}"
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
        """Populates dictionaries using data from the API call"""
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
        """Returns average of stars"""
        average_stars = total_stars / total_repos
        return average_stars

    def get_median_stars(stars):    
        """Returns median of stars using statistics module"""
        median_stars = st.median(stars)
        return median_stars

    def create_graph(repo_links, stars, hover_texts, average_stars, median_stars):
        """Uses plotly to create a bar graph with features such as hyperlink and hovertext"""
        #creates a bar graph of the most popular APIS
        title = f"Most-Starred {programming_language.title()} Projects on GitHub"
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
                #wrapping with [] turns the item into a list
                #multiplying by len(repo_links) gives us that many indexes
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

    #function calls
    try:
        target_language = create_ui()
        print("Target language: " + repr(target_language))
        #print("Num stars: " + num_stars)
        target_code = translation(target_language)
        repo_dicts = api_call()
        populated_dicts = populate_dicts(target_code, repo_dicts)
        average_stars = get_average_stars(populated_dicts[0], populated_dicts[1])
        median_stars = get_median_stars(populated_dicts[4])
            #populated_dicts = [total_stars, total_repos, repo_links, hover_texts, stars]
            #create_graph(repo_links, stars, hover_texts, average_stars, median_stars):
        create_graph(populated_dicts[2], populated_dicts[4], populated_dicts[3], average_stars, median_stars)
    #exception is stored as e
    except Exception as e:
        #shows the error so we understand whats wrong
        messagebox.showerror("Error", e)