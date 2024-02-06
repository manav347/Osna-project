from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
print(excel.sheetnames)
sheet = excel.active    
sheet.title= 'User'
sheet.append(['nameFollower','nameFollowing'])

print('Enter the user name you want to extract: ')

try:
    #                      https://github.com/manavp347?tab=followers
    source = requests.get('https://github.com/manav347?tab=followers')
    source.raise_for_status()

    soup = BeautifulSoup(source.text,'html.parser')
    # print(soup)

    followers = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

    for follower in followers:

        # name = follower.find('span', class_="Link--secondary").text
        nameFollower=follower.text
        print(follower.text)
        
        sheet.append([nameFollower])


    ########   FOLLOWING       ###############

    source = requests.get('https://github.com/manav347?tab=following')
    source.raise_for_status()

    soup = BeautifulSoup(source.text,'html.parser')
    # print(soup)

    followings = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

    for following in followings:

        # name = follower.find('span', class_="Link--secondary").text
        nameFollowing=following.text
        print(following.text)
        
        sheet.append(['B',nameFollowing])

except Exception as e:
    print(e)


excel.save('User_list.xlsx')