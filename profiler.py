import requests
from bs4 import BeautifulSoup

def scrapeInstagram(soup1):
    insta_Data = []
    main_Data = []
    main_Profile = []
    for meta in soup1.find_all(name="meta", attrs={"property": "og:title"}):
        main_Data = meta['content'].split()
    for meta in soup1.find_all(name="meta", attrs={"property": "og:description"}):
        insta_Data = meta['content'].split()
    for meta in soup1.find_all(name="meta", attrs={"property": "og:url"}):
        main_Profile = meta['content'].split()

    url = main_Profile[0]
    followers = insta_Data[0]
    following = insta_Data[2]
    posts = insta_Data[4]
    fname = main_Data[0]
    lname = main_Data[1]


    # Printing the results
    print("\nINSTAGRAM ACCOUNT NANE:", fname + lname)
    print("\nINSTAGRAM USERNAME :   ", insta_User)
    print("\nNo OF POSTS        :   ", posts)
    print("\nNo OF FOLLOWERS    :   ", followers)
    print("\nNo OF FOLLOWING    :   ", following)
    print("\nPROFILE LINK       :   ", url)

# Driver Code
if __name__ == '__main__':

    myfile = open("usernames.txt","r")
    username = myfile.read()

    # Prompting the user to enter the INSTAGRAM USERNAME
    insta_User = username

    # Storing the complete URL with user-input INSTAGRAM USERNAME
    insta_URL = "https://www.instagram.com/" + insta_User

    # Sending request to the above URL and storing the response in insta_Page
    insta_Page = requests.get(insta_URL)


    soup = BeautifulSoup(insta_Page.text, "html.parser")


    scrapeInstagram(soup)
