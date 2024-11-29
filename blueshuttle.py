from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime, timedelta,time
import json
import random
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

shuttleurl = 'http://127.0.0.1:8000/admin/' 
driver.get(shuttleurl)
sleep(1)
username = driver.find_element(By.NAME,'username')
username.send_keys('Subesh')
password = driver.find_element(By.NAME,'password')
password.send_keys('Subesh@123')
login_button = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input')
login_button.click()
sleep(1)
blueshuttle_entry = driver.find_element(By.XPATH, '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/td[1]/a')
blueshuttle_entry.click()
sleep(1)
current_time = datetime.combine(datetime.today(), time(7, 0))
for i in range(581):  # Loop 20 times
    try:
        
        time_str = current_time.strftime('%H:%M')  # Keep 24-hour format for morning times

        # Find the time entry field and enter the current time
        time_entry_field = driver.find_element(By.XPATH, '//*[@id="id_time"]')  # Update to the correct name or XPath
        time_entry_field.clear()
        time_entry_field.send_keys(time_str)
        current_time += timedelta(minutes=random.randint(1, 2))
        # Click the blueshuttle entry
        # Set a random number of passengers in
        number_of_passangers_in = driver.find_element(By.NAME, 'number_of_passangers_in')
        number_of_passangers_in.clear()
        value_element_available = driver.find_element(By.XPATH, '//*[@id="blueshuttle_form"]/div/fieldset/div[6]/div/div/div')
        value_text_available = value_element_available.text
        random_passengers_in = random.randint(0, min(15, int(value_text_available)))
        number_of_passangers_in.send_keys(str(random_passengers_in))

        # Get the value of the occupancy field
        value_element_occupancy = driver.find_element(By.XPATH, '//*[@id="blueshuttle_form"]/div/fieldset/div[5]/div/div/div')
        value_text = value_element_occupancy.text

        try:
            value_integer = int(value_text)
        except ValueError:
            print("The value is not a valid integer.")
            value_integer = 0

        # Set a random number of passengers out if occupancy is greater than 0
        number_of_passangers_out = driver.find_element(By.NAME, 'number_of_passangers_out')
        number_of_passangers_out.clear()
        if value_integer > 0:
            random_passengers_out = random.randint(0, min(15, value_integer - 1))
        else:
            random_passengers_out = 0
        number_of_passangers_out.send_keys(str(random_passengers_out))
        

        # Submit the form and add another entry
        submit_button_add_another = driver.find_element(By.XPATH, '//*[@id="blueshuttle_form"]/div/div/input[2]')
        submit_button_add_another.click()
        sleep(1)

    except NoSuchElementException as e:
        print(f"Element not found in iteration {i + 1}: {e}")
        break  # Stop the loop if an essential element is not found
    except StaleElementReferenceException as e:
        print(f"Stale element in iteration {i + 1}: {e}")
        sleep(2)  # Wait briefly before retrying
        continue  # Skip to the next iteration if element is stale
    except Exception as e:
        print(f"An error occurred in iteration {i + 1}: {e}")
        break  # Stop the loop for other critical errors