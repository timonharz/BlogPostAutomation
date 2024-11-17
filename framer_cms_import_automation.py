import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


from gmail_api_inbox_reader import get_last_email

def import_csv_file_to_cms(csv_file_path):
    #Open framer.com login page
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get("https://framer.com/login")
    
    email_address = "tiharz18@gmail.com"
    
    #Tap on the continue with Google button
    try:
        # Use WebDriverWait to wait for the button to be visible and clickable
        button = driver.find_element(By.XPATH, "//button[span[text()='Continue with email']]")

        # Click the button
        button.click()  
        
        time.sleep(2)
        
        email_field = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
        email_field.send_keys(email_address)
        
        email_field.send_keys(Keys.RETURN)        
        
        
        continue_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
        continue_button.click()   
        
        last_email = get_last_email()
        
        
    except Exception as e:
        print(f"Error: {e}")
      
    time.sleep(100)  
    # Sign in with Google account
    
        
    


if __name__ == "__main__":
    import_csv_file_to_cms("data/blog_posts.csv")