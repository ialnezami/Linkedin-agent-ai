import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedinManager import LinkedInManager
class LinkedInBot:
    def __init__(self, profile_url, cookies_file="linkedin_cookies.pkl"):
        self.profile_url = profile_url
        self.driver = webdriver.Firefox()
        self.linkedInManager = LinkedInManager()
        
        self.login()

    def login(self):
        """Log in to LinkedIn using cookies."""
        self.driver.get("https://www.linkedin.com/login")
        # Load cookies
        try:
            with open(cookies_file, "rb") as file:
                self.cookies = pickle.load(file)
        except Exception as e:
            self.save_cookies()
        # Add cookies to the session
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()
        with open("linkedin_cookies.pkl", "wb") as cookiesfile:
            pickle.dump( self.driver.get_cookies(), cookiesfile)
        print("Logged in successfully.")

    def post(self):
        """Post content on LinkedIn."""
        # Ensure login and navigate to home
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "global-nav")))
        self.driver.get("https://www.linkedin.com/feed/")
        
        # Start a post
        start_post_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-box-feed-entry')]"))
        )
        start_post_button.click()
        
        # Enter content
        post_textbox = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ql-editor"))
        )
        content = self.linkedInManager.generate_new_post()
        self.driver.execute_script("arguments[0].innerHTML += arguments[1];", post_textbox, content)
        
        # Find and click the "Post" button
        post_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action artdeco-button')]"))
        )
        # post_button.click()
        print("Content posted successfully.")

    def comment_on_feed(self):
        """Comment on the first 5 posts in the LinkedIn feed."""
        self.driver.get("https://www.linkedin.com/feed/")
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "global-nav")))
        
        for i in range(5):
            try:
                # Locate post content
                post_content = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"(//div[contains(@class, 'feed-shared-update-v2__description')]//span)[{i + 1}]"))
                ).text
                print("Post content:", post_content)

                # Generate comment based on post content
                comment = self.linkedInManager.generate_comment(post_content)
                print("Generated comment:", comment)

                # Click comment button
                comment_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"(//button[contains(@aria-label, 'Comment')])[{i + 1}]"))
                )
                comment_button.click()

                # Enter and submit comment
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"(//div[contains(@class, 'comments-comment-box__editor')])[{i + 1}]"))
                )
                comment_box.click()
                comment_box.send_keys(comment)
                comment_box.send_keys(Keys.RETURN)
                
                time.sleep(2)  # Optional delay to mimic human behavior

            except Exception as e:
                print(f"Could not comment on post {i + 1}: {e}")
        
        print("Commented on the first 5 posts successfully.")

    def get_all_postsss(self):
        """Get all posts from the LinkedIn profile."""
        self.driver.get(self.profile_url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "main")))

        posts = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            post_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")
            for post in post_elements:
                try:
                    post_content = post.find_element(By.XPATH, ".//span[contains(@class, 'break-words')]").text
                    posts.append(post_content)
                except Exception as e:
                    print(f"Could not extract content from post: {e}")

            # Scroll down to load more posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Fetched all posts successfully.")
        return posts

    def get_all_posts(self):
        """Get all posts from the LinkedIn recent activity feed."""
        # Navigate to the specific recent activity page
        self.driver.get(self.profile_url)
        
        # Use a more general element to wait for page loading
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-finite-scroll__content"))
        )

        posts = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Find all posts within the loaded content class .break-words.tvm-parent-container
            post_elements = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'break-words')]")
            for post in post_elements:
                try:
                    # Extract the post content (using a general XPath that may adapt better to LinkedIn's structure)
                    post_content = post.find_element(By.XPATH, ".//span[contains(@class, 'break-words')]").text
                    posts.append(post_content)
                except Exception as e:
                    print(f"Could not extract content from post: {e}")
                    break

            # Scroll down to load more posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)

            # Check for page scroll completion
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the end of the page.")
                break
            last_height = new_height

        print("Fetched all posts successfully.")
        print(posts)
        return posts

    def close(self):
        """Close the browser."""
        self.driver.quit()
        print("Browser closed.")

    def save_cookies(self, cookies_file="linkedin_cookies.pkl"):
        driver = webdriver.Firefox()
        driver.get("https://www.linkedin.com/login")
        # Wait for the user to log in manually
        input("Please log in manually, then press Enter here to save cookies...")
        # Save cookies after manual login
        with open("linkedin_cookies.pkl", "wb") as cookiesfile:
            pickle.dump(driver.get_cookies(), cookiesfile)
        driver.quit()
        print("Cookies saved successfully.")



