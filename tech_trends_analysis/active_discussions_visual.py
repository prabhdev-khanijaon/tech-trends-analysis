from operator import itemgetter
import requests
import plotly.express as px


# Make an API call and check the response.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()

# Check how many submissions are present in submission_ids 
#   before iterating over them.
subids_length = len(submission_ids)
print(f"Number items present in submission_ids: {subids_length}")

submission_dicts = []

# Limit to top 50 stories.
for submission_id in submission_ids[:30] :
    # Make a new API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    # Catch KeyErrors incase a promotional post is submitted.
    try :
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }
        submission_dicts.append(submission_dict)
    except KeyError as ke :
        print(f"\tSubmission {submission_id} has encountered a KeyError: '{ke}'"
              )
        continue

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                          reverse=True)


# for submission_dict in submission_dicts :
#     print(f"\nTitle: {submission_dict['title']}")
#     print(f"Discussion link: {submission_dict['hn_link']}")
#     print(f"Comments: {submission_dict['comments']}")


# Process submission_dicts information for visualization.
submission_links, comments, hover_texts = [], [], []

for submission in submission_dicts :
    # Turn submission titles into active links.
    # Shorten long article titles.
    submission_title = submission['title'][:30]
    submission_url = submission['hn_link']
    submission_link = f"<a href='{submission_url}'>{submission_title}</a>"
    submission_links.append(submission_link)

    comments.append(submission['comments'])

    # Build hover texts.
    title = submission_title
    comment_qty = submission['comments']
    hover_text = f"{title}<br  />{comment_qty} comments"
    hover_texts.append(hover_text)

# Make visualization.
title = "Hacker News Top Articles - Top 30 Most Commented on"
labels = {'x': 'Articles', 'y': 'Comments count'}
fig = px.bar(x=submission_links, y=comments, title=title, labels=labels,
             hover_name=hover_texts)

fig.update_layout(title_font_size=28,
                  xaxis_title_font_size=20,
                  yaxis_title_font_size=20,
                  )

fig.update_traces(marker_opacity=0.8)

fig.show()
fig.write_html('ex_17_2_active_discussions_5.html')