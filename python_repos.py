import requests

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
repo_dicts = response_dict["items"]
print(f"Repositories returned: {len(repo_dicts)}")

#examines the first repository
repo_dict = repo_dicts[0]
print(f"\nKeys: {len(repo_dict)}")
for key in sorted(repo_dict.keys()):
    print(key)