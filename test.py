from bs4 import BeautifulSoup
import requests
import openpyxl

FollowerArray = []
FollowingArray = []

finalFollowerArray = []
finalFollowingArray = []
FinalUserArray = []  # Initialize outside the loop


def scrape_github_user_data(target_user, limit):
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


        follower_data = follower_data[:limit]
        print(f"Top 10 Followers of {target_user}:", follower_data)
        following_data = following_data[:limit]
        print(f"Top 10 Following  of {target_user}:", following_data)

        # Top 10 user's ID
        # print("\n")
        # follower_data_10 = follower_data[:10]
        # print(f"Top 10 Followers of {target_user}:", follower_data)
        # following_data_10 = following_data[:10]
        # print("Top 10 Following:", following_data)

        # Make a conditional loop for root user
        # for obj in follower_data_10:
        #     print(obj)
        #     follower_data, following_data = scrape_github_user_data(obj)
        #     save_to_excel(obj, follower_data, following_data)

        return follower_data, following_data

    except Exception as e:
        print(f"Error occurred while processing {target_user}: {e}")
        return [], []

def save_to_excel(target_user, follower_data, following_data, limit):
    global FinalUserArray  # Declare FinalUserArray as global

    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'User'

    FollowerArray.extend([follower_data,target_user])  # Extend the FollowerArray with follower_data
    FollowingArray.extend(following_data)  # Extend the FollowerArray with follower_data


    # for follower, target_user in zip(follower_data, target_user):
    #     FollowerArray.extend([follower, target_user])
    
    
    # for follower, target in zip(follower_data, target_user):
    #     FollowerArray.extend([follower, target])


    finalFollowerArray.extend(follower_data)  # Extend the FollowerArray with follower_data
    finalFollowingArray.extend(following_data)  # Extend the FollowerArray with follower_data


    # Extend the FinalUserArray with follower_data and following_data
    FinalUserArray.extend(follower_data)
    FinalUserArray.extend(following_data)

    # Convert FinalUserArray to set to get unique IDs, then back to list
    FinalUserArray = list(set(FinalUserArray))

    # # Print the FinalUserArray
    # print("\n")
    # print("FinalUserArray:", FinalUserArray)
    # print("\n")
    # print("FinalUserArray:", len(FinalUserArray))
    # print("\n")
    # print("Len:", following_data)
    # print("Len:", follower_data)

    sheet.append(['Source','Target'])

    for follower in follower_data:
        sheet.append([follower,target_user])

    for following in following_data:
        sheet.append([target_user,following])

    excel.save(f'{target_user}_list.xlsx')



    # Print the FinalUserArray
    print("\n")
    print("FinalUserArray:", FinalUserArray)
    print("\n")
    print("FinalUserArray:", len(FinalUserArray))
    print("\n")

if __name__ == "__main__":
    
    # Take user input for the targeted user IDs separated by commas
    limit = int(input('Enter the upper limit of IDs: '))
    target_users = input('Enter the user IDs separated by commas: ').split(',')

    for target_user in target_users:
        follower_data, following_data = scrape_github_user_data(target_user.strip(), limit)
        save_to_excel(target_user.strip(), follower_data, following_data, limit)  # Pass both follower_data and following_data

    
    print("\n")
    print("\n")
    print("finalFollowerArray:", finalFollowerArray)
    print("\n")
    print("finalFollowingArray:", finalFollowingArray)

