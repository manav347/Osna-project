from bs4 import BeautifulSoup
import requests

# Initialize arrays to store follower and following data
FollowerArray = []
FollowingArray = []

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
        FollowerArray.append(name_follower)

    # Fetch following data
    following_url = f'https://github.com/{target_user}?tab=following'
    source = requests.get(following_url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')
    followings = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

    for following in followings:
        name_following = following.text
        FollowingArray.append(name_following)

except Exception as e:
    print(e)

# Compare arrays and store unique elements in FinalUserArray
FinalUserArray = list(set(FollowerArray + FollowingArray))

# Print the FinalUserArray
print("FinalUserArray:", FinalUserArray)
print("FinalUserArray:", len(FinalUserArray))
