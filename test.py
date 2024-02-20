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

        follower_data = [follower.text for follower in followers][:15]

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

def save_to_excel(user_data_dict):
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'User'
    sheet.append(['Source','Target'])
    for user, (follower_data, following_data) in user_data_dict.items():
        for follower in follower_data:
            sheet.append([follower, user])
        for following in following_data:
            sheet.append([user, following])
    excel.save('github_user_data.xlsx')

if __name__ == "__main__":
    # Take user input for the targeted user ID
    target_user = input('Enter the user ID: ').strip()

    # Scrape data for the initial user
    follower_data, following_data = scrape_github_user_data(target_user)

    # Create a set of all unique IDs
    unique_ids = set(follower_data + following_data + [target_user])

    # Initialize a dictionary to store user data
    user_data_dict = {}

    # Scrape data for each unique ID
    for user_id in unique_ids:
        follower_data, following_data = scrape_github_user_data(user_id)
        user_data_dict[user_id] = (follower_data, following_data)

    # Save all data to a single Excel sheet
    save_to_excel(user_data_dict)

    print("Data saved to github_user_data.xlsx")
