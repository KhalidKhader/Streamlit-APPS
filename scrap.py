# import streamlit as st
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# # Define the web scraping function with headers
# def scrape_website(url):
#     # Setting a custom user-agent to mimic a browser
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise HTTPError for bad responses
#         soup = BeautifulSoup(response.content, 'html.parser')
#         return soup
#     except requests.exceptions.HTTPError as err:
#         st.error(f"HTTP error occurred: {err}")
#     except Exception as err:
#         st.error(f"An error occurred: {err}")
#     return None

# # Streamlit app UI
# st.title('Web Scraping with Streamlit')

# url = st.text_input('Enter the URL of the website to scrape:')
# soup_items = st.text_input('Enter the Items you want to scrape:')
# soup_items = soup_items.split(',')

# if st.button('Scrape'):
#     if url:
#         soup = scrape_website(url)
#         if soup:
#             # st.write(soup.prettify())
#             items = soup.find_all(soup_items)
#             print(items)
#             for header in items:
#                 st.write(header.text)
#     else:
#         st.warning('Please enter a valid URL.')
        
# if st.button('Save to CSV'):
#     try:
#         pd.to_csv('/your_scraped_data_to_csv')
#     except:
#         st.write('Faild to save the data')
    
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the web scraping function with headers
def scrape_website(url):
    # Setting a custom user-agent to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Streamlit app UI
st.title('Web Scraping with Streamlit')

url = st.text_input('Enter the URL of the website to scrape:')
soup_items = st.text_input('Enter the tags you want to scrape (comma-separated):')

scraped_data = []

if st.button('Scrape'):
    if url and soup_items:
        soup = scrape_website(url)
        if soup:
            # Find all elements with the specified tags
            for tag in soup_items.split(','):
                tag = tag.strip()
                items = soup.find_all(tag)
                
                if items:
                    for item in items:
                        scraped_data.append(item.text.strip())
                        st.write(item.text.strip())
                else:
                    st.warning(f"No elements found for tag: {tag}")
    else:
        st.warning('Please enter a valid URL and tags to scrape.')

# Save the scraped data to CSV
if st.button('Save to CSV'):
    if scraped_data:
        # Create a DataFrame from the scraped data
        df = pd.DataFrame(scraped_data, columns=['Scraped Data'])
        
        # Save DataFrame to CSV
        csv_filename = 'scraped_data.csv'
        try:
            df.to_csv(csv_filename, index=False)
            st.success(f'Data saved to {csv_filename}')
            st.write(df)
        except Exception as e:
            st.error(f'Failed to save the data: {e}')
    else:
        st.warning('No data to save. Please scrape data first.')

