#/bin/python

from bs4 import BeautifulSoup
import requests
import time
'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC'''


url = 'https://www.gigsalad.com/services'
base_url = 'https://www.gigsalad.com'

clean_links = set()

# Send a GET request to the URL and retrieve the page content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all anchor tags (links) in the parsed HTML
services_links = soup.find_all('a', href=True)

# Extract and clean the links
for link in services_links:
    href = link.get('href')
    if '/book' in href:
        print(href)
        clean_links.add(base_url + href)



clean_links = list(clean_links)

music_links = set()
speaker_links = set()

srvc_links = set()

for link in clean_links:
	if 'music' in link:
		music_categories = requests.get(link)
		soup = BeautifulSoup(music_categories.text, 'html.parser')
		categories = soup.find_all('ul', class_='column')
		#print(categories)
		for item in categories:
			musicians = item.find_all('a', href=True)
			for artist in musicians:
				refs = artist.get('href')
				music_links.add(base_url + refs)
				#print(refs)
				

	elif 'speaker' in link:
		speaker_categories = requests.get(link)
		soup = BeautifulSoup(speaker_categories.text, 'html.parser')
		spk_div = soup.find_all('div', class_='category-listing__heading')
		for div in spk_div:
			title = div.find('h2')
			spk_title = title.text
		categories = soup.find_all('ul', class_='column')
		#print(categories)
		for item in categories:
			speakers = item.find_all('a', href=True)
			for speaker in speakers:
				refs = speaker.get('href')
				speaker_links.add(base_url + refs)
				#print(refs)

	#visit /book-entertainer
	elif 'entertainer' in link:
		entalinks = []
		ent_categories = requests.get(link)
		soup = BeautifulSoup(ent_categories.text, 'html.parser')

		#find div for each row of ent. class(actors, most  popular etc)
		ent_div = soup.find_all('div', class_='small-up-1')
		
		for div in ent_div:

			#find the category name (magic, most popular, etc)
			head = div.find('div', class_='category-listing__heading')
			ent_head = head.find('h2').text	
						
			#ul for items in each category
			categories = div.find_all('ul', class_='column')
			
			#find link for eash item
			for item in categories:	
				entertainer = item.find_all('a', href=True)

				#extract link for each categ item
				for ent in entertainer:
					ent_title = ent.text
					refs = ent.get('href')
					
					all_links = {ent_head: {ent_title: base_url + refs}}
					entalinks.append(all_links)

			


	elif 'service' in link:
		srv_categories = requests.get(link)
		soup = BeautifulSoup(srv_categories.text, 'html.parser')	
		categories = soup.find_all('ul', class_='column')
		#print(categories)
		for item in categories:
			srvc = item.find_all('a', href=True)
			for srv in srvc:
				refs = srv.get('href')
				srvc_links.add(base_url + refs)
				



enter_links = []
stat_titl = []
us_links = []
loc_entalinks = {}
ent_names = []
categry_list = []



for i in entalinks:
	for categ, act in i.items():				
	
		for act_title, ur in act.items():
			if not act_title == 'See More':

				enter_links.append(ur)
				
				resp = requests.get(ur)
				act_soup = BeautifulSoup(resp.text, 'html.parser')

				state_div = act_soup.find('div', id='choose_state')

				if state_div:
					print('\n', categ, '\n')
					print(act_title, '\n')
					
					heading = state_div.find('h5').text
					
					print(heading, '\n')
					us_cat_list = []
					cad_cat_list = []		
					#find country
					country_title = state_div.find_all('h4')
					for country in country_title:
						if country.text == 'United States:':
							print(country.text, '\n')

							#find links in us
							child = country.find_next_sibling()
							country_ul = child.find_all('ul', class_='medium-3')
							for li in country_ul:
								states_li = li.find_all('li', class_='js-show-container')

								#states link
								for states in states_li:
									state_anchor = states.find('a')
									state_name = state_anchor.text.strip()
									usa_ref = state_anchor.get('href')
									us_cat_list.append({state_name: base_url + usa_ref})
									
									print(usa_ref)
									print(state_name)
								
									
							print('\n')
							categry_list.append({categ: {act_title: {country.text: [k for k in us_cat_list] }}})
							
								


						else:
							print(country.text, '\n')
							child = country.find_next_sibling()
							country_ul = child.find_all('ul', class_='medium-3')
							for li in country_ul:
								states_li = li.find_all('li', class_='js-show-container')
								for states in states_li:
									state_anchor = states.find('a')
									state_name = state_anchor.text.strip()
									canada_refs = state_anchor.get('href')
									cad_cat_list.append({state_name: base_url + canada_refs})
									print(state_name)
									print(canada_refs)
									
							categry_list.append({categ: {act_title: {country.text: [k for k in cad_cat_list] }}})

						
				else:
					unsort_categ = []
					print('\n', categ, '\n')
					print(act_title, '\n')
					enta_div = act_soup.find_all('div', class_='vendor-card-list')
					for div in enta_div:
						person = div.find_all('article', class_='vendor-card')
						for man in person:
							name = man.find('h3')
							lnk = name.find('a')
							rf = lnk.get('href')
							unsort_categ.append({name.text: base_url + rf})
							print(name.text)
							print(rf)
					categry_list.append({categ: {act_title: [m for m in unsort_categ]}})		
							


print(categry_list)
	

