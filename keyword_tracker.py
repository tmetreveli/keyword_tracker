import importlib
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Define search parameters
language_code = 'en'
search_query = input('Enter a key: ')
number_of_results = 10

# Define request headers
headers = {
  # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJkZDU5MjQxNWExNTg5MjgxNDA0YTc0YjFmYzBhMDEyMyIsImp0aSI6ImIzZGQxNDYwNjY4ODAwOTIwNzljMDIzN2E2Mzc5NGZmZmJiNDc1NWZiZTQzNTYxZDY3MmJkN2VkZjQzMWM5ODU5NjMyMTBiMzhlZjMxYTM2IiwiaWF0IjoxNjk0NDQxNzgxLjA4MDQzOCwibmJmIjoxNjk0NDQxNzgxLjA4MDQ0MiwiZXhwIjozMzI1MTM1MDU4MS4wNzgwNjQsInN1YiI6IjczNzM1MTU5IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.Pz5nrJuY6HgQ70hU7tCEq6eBxpDtVVH180I1C1vEeVmNK3-n38sKtjGKoQ2FYUCnKRvoZt1qcFHkV37ShPZPMSj-RBXFXb15D9CyiNSOctMEcq95ttjf-RirUDsrdpr6wxlOiptsOYhZhSqmTv3pqF_hCGqUYmB_QnE_iC6asmKRivSHb5jvw77Lgaq_O-x-n4JkR8LN7Ch-s45l9jqrXwLm6xCFJ4Z6_Wa3H852tDCvI1qjoxZAlYI-BRthnEj275gu-sucV8S4YMrCiQNB_kpXO65ptbcC6xlaT3Nz9IS27ora_WU13j1w6N4tzUYPQWwRQNG5-mGDQznPYfcTcrI20e0kyO-Pxfa-09Eh9ccI6yd_U8R6TEgsxliee-xz3CIGJC6zGHlwMwrKW4Qz78fKtPj7bbtlNU9UeG6fGPW1ahP7vL5JOTIJbkL0aZn2PUtCa_pY3o4o84yPQh7_R024vwVPFYb9_1fudOP-n_SGbVXDCZ0YXnlM8IPcGxPuCqiVzKIHLmbV_A7A6wbaVQ1ibkcf1jzl9MACLq5HxcKp02stW_i76V1W7RwLjkmJmyzwUOQE9FGQWTVEzwLY6CB1h5EXeik38ysmO_ojp4djllBkdk3hKuAVaVgVjyp9inDvsZOsICzB7tupkHfgjpIYeQjNzXtlH2nWnq09MuQ'
}

# Build API endpoint URL
base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
endpoint = '/search/page'
url = base_url + language_code + endpoint
parameters = {'q': search_query, 'limit': number_of_results}

# Make API call to search Wikipedia
response = requests.get(url, headers=headers, params=parameters)

# Parse JSON response
response = json.loads(response.text)

# Extract URLs from response
urls = []
for page in response['pages']:
  display_title = page['title']
  article_url = 'https://' + language_code + '.wikipedia.org/wiki/' + page['key']
  try:
    article_description = page['description']
  except:
    article_description = 'a Wikipedia article'
  try:
    thumbnail_url = 'https:' + page['thumbnail']['url']
  except:
    thumbnail_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png'
  urls.append(article_url)  

# Fetch the content of the first URL
response = requests.get(urls[0])
page_content = response.text

# Parse HTML content
soup = BeautifulSoup(page_content, 'html.parser')
article_text = soup.get_text()

# Initialize word count dictionary
word_count = {}
stop_words = set(stopwords.words('english'))
words = []

# Extract text and count word frequencies
for paragraph in soup.find_all('p'):  # Find all paragraph tags
    paragraph_text = paragraph.text.lower()
    clean_text = re.sub(r'[^\w\s]', '', paragraph_text)
    words += clean_text.split()

for word in words:
  if word not in word_count:
    word_count[word] = 1
  else:
    word_count[word] += 1


filtered_word_count = {word: count for word, count in word_count.items() if word.lower() not in stop_words}

# Sort dictionary by frequency
sorted_dict = {k: v for k, v in sorted(filtered_word_count.items(), key=lambda item: item[1], reverse=True)}

# Get the top 5 most frequent words
most_common_used = []
times = 0
for key in sorted_dict:
  most_common_used.append((key,sorted_dict[key]))
  times += 1
  if times >=5:
    break

# Prepare data for visualization
top_5_words = [word for word, count in most_common_used[:5]]
top_5_counts = [count for word, count in most_common_used[:5]]

# Plot the data
plt.figure(figsize=(10,6))
plt.barh(top_5_words, top_5_counts, color='purple')
plt.xlabel('Frequency')
plt.ylabel('Words')
plt.title('Top 5 Most Common Words')
plt.show()


plt.figure(figsize=(8, 8))

# Creating the pie chart
plt.pie(top_5_counts, labels=top_5_words, autopct='%1.1f%%', startangle=140)

# Adding a title
plt.title('Top 5 Most Common Words Distribution')

# Displaying the chart
plt.show()
