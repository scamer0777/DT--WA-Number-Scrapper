import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get("https://web.whatsapp.com")
print("PLEASE SCAN THE QR CODE TO LOG IN INTO WHATSAPP")


time.sleep(50)  

try:
  
    title = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span').text
    new_participants = [item.strip() for item in title.split(',')]

    
    new_participants = [item.replace('+91', '').replace(' ', '') for item in new_participants]

    unique_participants = []

    
    if os.path.exists('group.csv'):
        existing_participants = pd.read_csv('group.csv', header=None)[0].tolist()

        
        unique_participants = [p for p in new_participants if p not in existing_participants]

    else:
        unique_participants = new_participants
        existing_participants = []  

    
    if unique_participants:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_csv_filename = f'new_participants_{timestamp}.csv'
        
        with open(new_csv_filename, 'w') as f:
            for participant in unique_participants:
                f.write(participant + '\n')
        
        print(f"New participants saved to {new_csv_filename}")

       
        all_participants = existing_participants + unique_participants
        with open('group.csv', 'w') as f:
            for participant in all_participants:
                f.write(participant + '\n')
        
        print(f"group.csv updated with the latest participants")
    else:
        print("No new unique participants found.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
   
    driver.quit()