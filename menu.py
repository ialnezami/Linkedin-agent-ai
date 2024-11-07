from LinkedInBot import LinkedInBot
def show_menu():
    print("\nLinkedIn Bot - Menu")
    print("1. Log in to LinkedIn")
    print("2. Post on LinkedIn")
    print("3. Comment on feed posts")
    print("4. Get all my posts")
    print("5. Save cookies(first time to be connected easily )")
    print("9. Exit")
    return input("Choose an option (1-5): ")

def main():
    profile_url = "https://www.linkedin.com/in/ialnezami/recent-activity/all/"  # Replace with your actual profile URL
    bot = LinkedInBot(profile_url)
    while True:
        choice = show_menu()
        if choice == "1":
            bot.login()
        elif choice == "2":
            bot.post()
        elif choice == "3":
            bot.comment_on_feed()
        elif choice == "4":
            posts = bot.get_all_posts()
            print("All Posts:")
            for post in posts:
                print(post)
        elif choice == "5":
            bot.save_cookies()
        elif choice == "9":
            print("Exiting...")
            bot.close()
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()