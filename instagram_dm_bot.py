import os
import time
import random
import logging
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import pyautogui
from datetime import datetime, timedelta
from config import *
from getpass import getpass
import random
import string

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InstagramDMBot:
    def __init__(self):
        self.driver = None
        self.ua = UserAgent()
        self.dms_sent = 0
        self.last_dm_time = None
        self.setup_driver()
        self.session_start_time = datetime.now()
        self.total_actions = 0
        self.last_action_time = None

    def setup_driver(self):
        """Initialize undetected Chrome driver with random user agent and anti-detection measures"""
        options = uc.ChromeOptions()
        
        # Random user agent
        options.add_argument(f'user-agent={self.ua.random}')
        
        # Additional anti-detection measures
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        
        # Add random window size variation
        screen_width, screen_height = pyautogui.size()
        window_width = int(screen_width * random.uniform(0.85, 0.95))
        window_height = int(screen_height * random.uniform(0.85, 0.95))
        
        if HEADLESS:
            options.add_argument('--headless')
        
        try:
            self.driver = uc.Chrome(options=options)
            
            # Set window size and position
            window_x = int((screen_width - window_width) / 2)
            window_y = int((screen_height - window_height) / 2)
            self.driver.set_window_size(window_width, window_height)
            self.driver.set_window_position(window_x, window_y)
            
            # Add random mouse movements to appear more human-like
            self.random_mouse_movement()
            
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise

    def random_mouse_movement(self):
        """Simulate random mouse movements with natural acceleration and deceleration"""
        screen_width, screen_height = pyautogui.size()
        for _ in range(random.randint(2, 4)):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            duration = random.uniform(0.2, 0.5)
            pyautogui.moveTo(x, y, duration=duration)
            time.sleep(random.uniform(0.1, 0.3))

    def human_like_typing(self, element, text):
        """Simulate human-like typing with random delays and occasional mistakes"""
        for char in text:
            # Random chance to make a typo and correct it
            if random.random() < 0.05:  # 5% chance of typo
                wrong_char = random.choice(string.ascii_lowercase)
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys('\b')  # Backspace
                time.sleep(random.uniform(0.1, 0.3))
            
            element.send_keys(char)
            # Vary typing speed
            time.sleep(random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX))
            
            # Occasionally pause longer to simulate thinking
            if random.random() < 0.1:  # 10% chance of pause
                time.sleep(random.uniform(0.5, 1.5))

    def random_scroll(self):
        """Perform random scrolling to simulate human behavior"""
        try:
            scroll_amount = random.randint(100, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
        except:
            pass

    def check_rate_limits(self):
        """Check and enforce rate limits"""
        current_time = datetime.now()
        
        # Check hourly limit
        if self.dms_sent >= MAX_DMS_PER_HOUR:
            if self.last_dm_time and current_time - self.last_dm_time < timedelta(hours=1):
                wait_time = 3600 - (current_time - self.last_dm_time).seconds
                logger.info(f"Rate limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                self.dms_sent = 0
        
        # Check session duration
        session_duration = current_time - self.session_start_time
        if session_duration > timedelta(hours=MAX_SESSION_HOURS):
            logger.info("Maximum session duration reached. Taking a break...")
            time.sleep(random.uniform(1800, 3600))  # 30-60 minute break
            self.session_start_time = current_time
            self.dms_sent = 0
        
        # Check action frequency
        if self.last_action_time:
            time_since_last_action = (current_time - self.last_action_time).seconds
            if time_since_last_action < MIN_ACTION_INTERVAL:
                wait_time = MIN_ACTION_INTERVAL - time_since_last_action
                time.sleep(wait_time)
        
        self.last_action_time = current_time

    def wait_and_click(self, by, value, timeout=10):
        """Wait for element and click it with human-like behavior"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            
            # Random mouse movement before clicking
            self.random_mouse_movement()
            
            # Scroll element into view if needed
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(0.5, 1.0))
            
            # Click with random delay
            time.sleep(random.uniform(0.2, 0.5))
            element.click()
            
            # Update action counter
            self.total_actions += 1
            
            return True
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {value}")
            return False

    def login(self):
        """Handle Instagram login"""
        try:
            self.driver.get(LOGIN_URL)
            time.sleep(random.uniform(2, 4))
            
            # Hardcoded credentials
            username = "yourusername@gmail.com"
            password = "yourpassword"
            
            # Wait for username field and enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
            )
            self.human_like_typing(username_field, username)
            time.sleep(random.uniform(1, 2))
            
            # Wait for password field and enter password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            self.human_like_typing(password_field, password)
            time.sleep(random.uniform(1, 2))
            
            # Click login button
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            login_button.click()
            
            # Wait for login to complete
            time.sleep(random.uniform(5, 7))
            
            # Check if login was successful
            try:
                # Wait for either the home icon or the "Save Info" button
                WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Home']")),
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save Info')]")),
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not Now')]")),
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Turn on Notifications')]"))
                    )
                )
                
                # Handle various popups
                popup_buttons = [
                    "//button[contains(text(), 'Not Now')]",
                    "//button[contains(text(), 'Turn on Notifications')]",
                    "//button[contains(text(), 'Save Info')]"
                ]
                
                for button_xpath in popup_buttons:
                    try:
                        button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, button_xpath))
                        )
                        button.click()
                        time.sleep(2)
                    except:
                        continue
                
                logger.info("Login successful!")
                # Add a longer delay after successful login
                time.sleep(10)
                return True
            except TimeoutException:
                logger.error("Login failed. Please check your credentials.")
                return False
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    def check_session(self):
        """Check if we're still logged in and relogin if needed"""
        try:
            # Check for common elements that indicate we're logged out
            logout_indicators = [
                "//input[@name='username']",  # Login username field
                "//input[@name='password']",  # Login password field
                "//button[contains(text(), 'Log in')]",  # Login button
                "//a[contains(text(), 'Log in')]",  # Login link
                "//h2[contains(text(), 'Log in to Instagram')]"  # Login header
            ]
            
            for indicator in logout_indicators:
                try:
                    if self.driver.find_element(By.XPATH, indicator).is_displayed():
                        logger.info("Session expired, attempting to relogin...")
                        return self.login()
                except:
                    continue
            
            # Additional check for home page elements
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Home']"))
                )
                return True
            except:
                logger.info("Home icon not found, attempting to relogin...")
                return self.login()
                
        except Exception as e:
            logger.error(f"Error checking session: {str(e)}")
            return self.login()

    def send_dm(self, username, message):
        """Send DM to a specific user with enhanced anti-detection measures"""
        try:
            # Check rate limits
            self.check_rate_limits()
            
            # Check session before proceeding
            if not self.check_session():
                logger.error("Failed to maintain session")
                return False
            
            # Visit user profile with random delay
            profile_url = f"{INSTAGRAM_URL}/{username}/"
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))
            
            # Check session again after page load
            if not self.check_session():
                logger.error("Session lost after page load")
                return False
            
            # Random scroll to appear more human-like
            self.random_scroll()
            
            # Check if profile exists and is accessible
            try:
                # Check for "Sorry, this page isn't available" message
                error_message = self.driver.find_elements(By.XPATH, "//h2[contains(text(), \"Sorry, this page isn't available\")]")
                if error_message:
                    logger.error(f"Profile {username} doesn't exist or is not accessible")
                    return False

                # Check for "This Account is Private" message
                private_account = self.driver.find_elements(By.XPATH, "//h2[contains(text(), 'This Account is Private')]")
                if private_account:
                    logger.error(f"Profile {username} is private")
                    return False

                # Try different selectors for the Message button
                message_button_selectors = [
                    "//div[text()='Message']",
                    "//div[contains(text(), 'Message')]",
                    "//button[contains(text(), 'Message')]",
                    "//a[contains(text(), 'Message')]",
                    "//div[@role='button' and contains(text(), 'Message')]"
                ]

                message_button = None
                for selector in message_button_selectors:
                    try:
                        message_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        if message_button:
                            break
                    except:
                        continue

                if not message_button:
                    # If direct message button not found, try the three-dot menu approach
                    logger.info("Direct Message button not found, trying three-dot menu...")
                    
                    try:
                        # Click the three-dot menu
                        three_dot_menu = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Options']"))
                        )
                        three_dot_menu.click()
                        time.sleep(2)

                        # Click the "Send message" button in the popup
                        send_message_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send message')]"))
                        )
                        send_message_button.click()
                        time.sleep(2)
                    except Exception as e:
                        logger.error(f"Failed to use three-dot menu: {str(e)}")
                        return False
                else:
                    # Click the direct message button if found
                    message_button.click()
                    time.sleep(2)

            except Exception as e:
                logger.error(f"Error accessing profile {username}: {str(e)}")
                return False

            # Wait for and handle notification popup
            try:
                # Wait for the notification popup
                notification_popup = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Turn on notifications')]"))
                )
                
                # Click "Turn On" button
                turn_on_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Turn On']"))
                )
                turn_on_button.click()
                time.sleep(2)
            except TimeoutException:
                logger.info("No notification popup found, continuing...")

            # Wait for message input and type message
            try:
                # Wait for the message input field
                message_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @aria-label='Message']"))
                )
                
                # Click the input field first
                message_input.click()
                time.sleep(1)
                
                # Type the message
                self.human_like_typing(message_input, message)
                time.sleep(1)
                
                # Find and click the send button
                send_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Send']"))
                )
                send_button.click()
                
                # Update counters
                self.dms_sent += 1
                self.last_dm_time = datetime.now()

                # Random delay before next message
                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                logger.info(f"Waiting {delay:.2f} seconds before next message...")
                time.sleep(delay)

                return True

            except TimeoutException as e:
                logger.error(f"Timeout while trying to send message: {str(e)}")
                return False

        except Exception as e:
            logger.error(f"Error sending DM to {username}: {str(e)}")
            return False

    def get_processed_profiles(self):
        """Get list of already processed profiles from output CSV"""
        try:
            if os.path.exists(OUTPUT_CSV):
                df = pd.read_csv(OUTPUT_CSV)
                return set(df['username'].tolist())
            return set()
        except Exception as e:
            logger.error(f"Error reading processed profiles: {str(e)}")
            return set()

    def process_csv(self):
        """Process the input CSV file with enhanced error handling and rate limiting"""
        try:
            # Read input CSV
            df = pd.read_csv(INPUT_CSV)
            
            # Get already processed profiles
            processed_profiles = self.get_processed_profiles()
            logger.info(f"Found {len(processed_profiles)} already processed profiles")
            
            # Filter out already processed profiles
            df = df[~df['username'].isin(processed_profiles)]
            
            if df.empty:
                logger.info("All profiles have been processed!")
                return
            
            # Shuffle the remaining dataframe to appear more random
            df = df.sample(frac=1).reset_index(drop=True)
            logger.info(f"Starting to process {len(df)} remaining profiles")
            
            results = []
            
            for index, row in df.iterrows():
                username = row['username']
                message = row['message']
                
                logger.info(f"Processing {username} ({index + 1}/{len(df)})...")
                
                # Add random delay between processing users
                time.sleep(random.uniform(5, 15))
                
                # Check session before processing each user
                if not self.check_session():
                    logger.error("Session check failed, attempting to relogin...")
                    if not self.login():
                        logger.error("Failed to relogin, stopping process")
                        # Save current progress before stopping
                        if results:
                            self.save_progress(results)
                        break
                
                success = self.send_dm(username, message)
                
                results.append({
                    'username': username,
                    'message': message,
                    'status': 'Success' if success else 'Failed',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # Save progress after each message
                self.save_progress(results)
                
                # Take occasional longer breaks
                if random.random() < 0.1:  # 10% chance
                    break_time = random.uniform(300, 600)  # 5-10 minutes
                    logger.info(f"Taking a longer break for {break_time:.0f} seconds...")
                    time.sleep(break_time)
                    
                    # Check session after long break
                    if not self.check_session():
                        logger.error("Session lost after break, attempting to relogin...")
                        if not self.login():
                            logger.error("Failed to relogin after break, stopping process")
                            break
                
        except Exception as e:
            logger.error(f"Error processing CSV: {str(e)}")
            # Save progress even if there's an error
            if results:
                self.save_progress(results)

    def save_progress(self, results):
        """Save progress to output CSV, merging with existing data"""
        try:
            # Read existing results if any
            if os.path.exists(OUTPUT_CSV):
                existing_df = pd.read_csv(OUTPUT_CSV)
                # Combine existing and new results
                combined_df = pd.concat([existing_df, pd.DataFrame(results)], ignore_index=True)
                # Remove duplicates keeping the latest entry for each username
                combined_df = combined_df.drop_duplicates(subset=['username'], keep='last')
            else:
                combined_df = pd.DataFrame(results)
            
            # Save to CSV
            combined_df.to_csv(OUTPUT_CSV, index=False)
            logger.info(f"Progress saved: {len(combined_df)} profiles processed")
            
        except Exception as e:
            logger.error(f"Error saving progress: {str(e)}")

    def cleanup(self):
        """Clean up resources with graceful shutdown"""
        try:
            # Add random delay before closing
            time.sleep(random.uniform(3, 7))
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

def main():
    bot = InstagramDMBot()
    try:
        if bot.login():
            logger.info("Starting/Resuming profile processing...")
            bot.process_csv()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main() 