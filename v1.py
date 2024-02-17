from bs4 import BeautifulSoup
import requests
import openpyxl

FollowerArray = []
FollowingArray = []
FinalUserArray = []  # Initialize outside the loop

def scrape_github_user_data(target_user):
    try:
        # Fetch followers data
        followers_url = f'https://github.com/{target_user}?tab=followers'
        source = requests.get(followers_url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')
        followers = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

        follower_data = [follower.text for follower in followers]

        # Fetch following data
        following_url = f'https://github.com/{target_user}?tab=following'
        source = requests.get(following_url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')
        followings = soup.find('turbo-frame', id="user-profile-frame").find_all('span', class_="Link--secondary")

        following_data = [following.text for following in followings]

        # print("\n")
        # print("FinalUserArray:", FinalUserArray)
        return follower_data, following_data

    except Exception as e:
        print(f"Error occurred while processing {target_user}: {e}")
        return [], []

def save_to_excel(target_user, follower_data, following_data):
    global FinalUserArray  # Declare FinalUserArray as global

    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'User'

    FollowerArray.extend(follower_data)  # Extend the FollowerArray with follower_data
    FollowingArray.extend(following_data)  # Extend the FollowerArray with follower_data

    # Extend the FinalUserArray with follower_data and following_data
    FinalUserArray.extend(follower_data)
    FinalUserArray.extend(following_data)

    # Convert FinalUserArray to set to get unique IDs, then back to list
    FinalUserArray = list(set(FinalUserArray))

    # Print the FinalUserArray
    print("\n")
    print("FinalUserArray:", FinalUserArray)
    print("Len:", following_data)
    print("Len:", follower_data)

    sheet.append(['nameFollower'])

    for follower in follower_data:
        sheet.append([follower])

    for following in following_data:
        sheet.append([following])

    excel.save(f'{target_user}_list.xlsx')



if __name__ == "__main__":
    # Take user input for the targeted user IDs separated by commas
    target_users = input('Enter the user IDs separated by commas: ').split(',')

    for target_user in target_users:
        follower_data, following_data = scrape_github_user_data(target_user.strip())
        save_to_excel(target_user.strip(), follower_data, following_data)  # Pass both follower_data and following_data

