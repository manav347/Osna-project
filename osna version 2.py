# This version gives the excel output according to the Source and Target nodes 

from bs4 import BeautifulSoup
import requests
import openpyxl

excel = openpyxl.Workbook()
sheet = excel.active    
sheet.title = 'User'
sheet.append(['Source', 'Target'])

# Take user input for the targeted user ID
target_user = input('Enter the user ID you want to extract: ')

try:
    # Fetch followers data
    followers_url = f'https://github.com/{target_user}?tab=followers'
    source = requests.get(followers_url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')
    followers = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

    for follower in followers:
        name_follower = follower.text
        sheet.append([name_follower,target_user])

    # Fetch following data
    following_url = f'https://github.com/{target_user}?tab=following'
    source = requests.get(following_url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')
    followings = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

    for following in followings:
        name_following = following.text
        sheet.append([target_user, name_following])

except Exception as e:
    print(e)

print(target_user)

excel.save(f'{target_user}_list.xlsx')
