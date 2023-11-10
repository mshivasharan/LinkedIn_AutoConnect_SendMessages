import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random


def random_sleep(range1, range2):
    # Generate a random number between 10 and 30
    sleep_time = random.randint(range1, range2)
    print(f"Sleeping for {sleep_time} seconds...")
    return sleep_time


def remove_delimiter_convert(input_file):
    # Replace with your CSV file's path
    # Open the input CSV file and read all rows into a string
    with open(input_file, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Read all rows into a string
        csv_data = '\n'.join(','.join(row) for row in csv_reader)

    # Split the input data into lines and remove any leading or trailing spaces
    lines = [line.strip() for line in csv_data.split('\n')]

    # Split each line on the semicolon and create a list of fields
    data = [line.split(';') for line in lines]

    # Create a CSV file and write the data
    with open('output.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row
        csv_writer.writerow(data[0][1:])  # Exclude the empty field at the beginning
        # Write the data rows
        for row in data[1:]:
            csv_writer.writerow(row[1:])

    print("CSV conversion complete. Output saved to 'output.csv'")
    return data


def login_credentials(linkedin_email, linkedin_password, chrome_driver_path):
    url = 'http://www.linkedin.com/login'

    #chromedriver path needs to be defined
    s = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-logging")
    driver = webdriver.Chrome(options=options, service=s)
    driver.get(url)

    # Wait for the "username" element to be visible and sleep for a random duration
    wait = WebDriverWait(driver, random_sleep(18,32)) 
    # Maximize the browser window
    driver.maximize_window() 

    username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")

    # Now you can interact with the elements
    username_input.send_keys(linkedin_email)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(random_sleep(2,8))
    return driver, wait


def connect_sendmessage(driver, wait):
    # Read the LinkedIn URLs from your CSV
    with open('output.csv', 'r') as csv_file:
        # Skip the header row if needed
        next(csv_file)
        for row in csv_file:
            data = row.split(',')
            linkedin_url = data[6]  # Adjust this based on the column index in your CSV

            if not (linkedin_url.startswith("https://www.linkedin.com") or linkedin_url.startswith("http://www.linkedin.com")):
                print(f"Invalid LinkedIn URL: {linkedin_url}")
                continue  # Skip this row and continue with the next one

            # Visit the LinkedIn profile
            try:
                driver.get(linkedin_url)
                time.sleep(random_sleep(2,8))
                all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button")))
                connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]
            
                if connect_buttons:
                    for btn in connect_buttons:
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(random_sleep(2,8))

                        add_note_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Add a note']")))
                        driver.execute_script("arguments[0].click();", add_note_button)
                        time.sleep(random_sleep(2,8))

                        # Input your customized message
                        message_input = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']")))
                        message = "Dear Miss/Mr. {}, I'm interested in connecting with you on LinkedIn. ...".format(data[0])
                        message_input.send_keys(message)
                        time.sleep(random_sleep(3,6))

                        send_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Send now']")))
                        driver.execute_script("arguments[0].click();", send_button)
                        close = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Dismiss']")))
                        driver.execute_script("arguments[0].click();", close)
                        time.sleep(random_sleep(5,10))

            except Exception as e:
                print(f"An error occurred while navigating to the LinkedIn profile: {e}")
                continue  # Skip this row and continue with the next one


#add input csv file location and call the function.
input_file = 'input.csv'                                         #provide the csv file with all the linkedIn links 
data = remove_delimiter_convert(input_file)

# Define your LinkedIn credentials
linkedin_email = "example@gmail.com"                                #your linkedIn email id
chrome_driver_path = r"C:/Program Files (x86)/chromedriver.exe"     #you should place this chromedriver.exe in a location and provide that location here
with open("password.txt") as PW:                                    #inside the password.txt add your password, just to make your password invisible in the code
    linkedin_password = PW.read().replace("\n", "")

# call the function
driver, wait = login_credentials(linkedin_email, linkedin_password, chrome_driver_path)
connect_sendmessage(driver, wait)

# Close the WebDriver when done
driver.quit()
