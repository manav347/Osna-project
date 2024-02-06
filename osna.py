from bs4 import BeautifulSoup
import requests
import openpyxl

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

        return follower_data, following_data

    except Exception as e:
        print(f"Error occurred while processing {target_user}: {e}")
        return [], []

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
    target_users = input('Enter the user IDs separated by commas: ').split(',')

    for target_user in target_users:
        follower_data, following_data = scrape_github_user_data(target_user.strip())
        save_to_excel(target_user.strip(), follower_data, following_data)
