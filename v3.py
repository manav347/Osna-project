from bs4 import BeautifulSoup
import requests

# Initialize arrays to store follower and following data
FollowerArray = []
FollowingArray = []

# Take user input for the targeted user ID
target_user = input('Enter the user ID you want to extract: ')

def scrape_github_user_data(target_user):
    print('I am here')
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
            print('following')
            FollowingArray.append(name_following)

    except Exception as e:
        print(e)

# Compare arrays and store unique elements in FinalUserArray
scrape_github_user_data(target_user)
FinalUserArray = list(set(FollowerArray + FollowingArray))

# Print the FinalUserArray
print("FinalUserArray:", FinalUserArray)
print("FinalUserArray:", len(FinalUserArray))


def save_to_excel(target_user, follower_data, following_data):
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'User'
    sheet.append(['nameFollower', 'nameFollowing'])

    for follower in follower_data:
        sheet.append([follower, ''])

    for following in following_data:
        sheet.append(['', following])

    excel.save(f'{target_user}_list.xlsx')

if __name__ == "__main__":
    # Take user input for the targeted user IDs separated by commas
    
    print('I am here 2')
    target_users = FinalUserArray

    for target_user in target_users:
        follower_data, following_data = scrape_github_user_data(target_user.strip())
        save_to_excel(target_user.strip(), follower_data, following_data)

