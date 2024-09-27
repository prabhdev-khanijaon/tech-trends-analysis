import requests
import plotly.express as px


# Make a list for the languages for the API call.
languages = ['javascript', 'ruby', 'c', 'java', 'perl', 'haskell', 'go']

# Dictionary to store responses for each language from API call.
all_responses = {}

# Loop through each language, make an API call and check the response.
for language in languages :
    url = "https://api.github.com/search/repositories"
    url += f"?q=language:{language}+sort:stars+stars:>10000"

    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)        
    print(f"Status code for {language}: {r.status_code}")

    if r.status_code == 200 :
        # Convert the response object to a dictionary.
        response_dict = r.json()

        # Add/update key:value pair to all_responses.
        all_responses[language] = response_dict

    else :
        print(f"Failed to retrieve data for {language}. Status code:" 
              f"{r.status_code}")

# Check if the API call processed all data successfully.
print(f"Complete results: {not response_dict['incomplete_results']}")

# Process repository information.
repo_dicts = all_responses.items()

repo_links, stars, hover_texts, repo_languages = [], [], [], []

for language, response_dict in  all_responses.items():
    repo_dicts = response_dict['items']
    for repo in repo_dicts :
        # Turn repo names into active links.
        repo_name = repo['name']
        repo_url = repo['html_url']
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)

        stars.append(repo['stargazers_count'])
        repo_languages.append(language)

        # Build hover texts.
        owner = repo['owner']['login']
        description = repo['description']
        hover_text = f"{language}<br  />{owner}<br />{description}"
        hover_texts.append(hover_text)

# Make visualization, color the bars according to it's language.
title = ("Most-Starred Non-Python Projects on GitHub")
labels = {'x': 'Repository', 'y': 'Stars', 'color': 'Programming Language'}
fig = px.bar(x=repo_links, y=stars, title=title, labels=labels,
             hover_name=hover_texts,
             color=repo_languages, 
             color_discrete_sequence=px.colors.qualitative.Bold)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
                  yaxis_title_font_size=20)

fig.update_traces(marker_opacity=0.6)

fig.show()
fig.write_html('ex_17_1_other_languages_4.html')