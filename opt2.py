from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Credentials
username = "CEC22CS029"
password = "myr1234@"

# Headless browser setup
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")

output = ""

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    # Step 1: Login
    driver.get("https://app.ktu.edu.in/login.htm")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "btn-login"))).click()

    # Step 2: Go to Student tab
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Student"))).click()

    # Step 3: Click "View Full Profile"
    wait.until(EC.presence_of_element_located((By.ID, "viewProfile"))).click()

    # Step 4: Click Exam / Result tab
    wait.until(EC.element_to_be_clickable((By.ID, "examResultTab"))).click()
    time.sleep(2)

    # Step 5: Scrape only first 2 Examination Grades (skip Revaluation)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    grade_buttons = soup.find_all("a", class_="btn btn-sm btn-primary")
    grade_links = [btn['href'] for btn in grade_buttons if "Examination Grades" in btn.get_text(strip=True)][:2]

    output += "\n First 2 Semester Examination Grades\n"
    output += "=" * 80 + "\n"

    for href in grade_links:
        driver.get("https://app.ktu.edu.in" + href)
        time.sleep(2)
        soup2 = BeautifulSoup(driver.page_source, "html.parser")
        table = soup2.find("table", class_="table table-bordered")

        if table:
            sem_title = soup2.find("h3").text.strip() if soup2.find("h3") else "Semester"
            output += f"\n {sem_title}\n"
            output += "-" * 70 + "\n"
            output += f"{'Subject':<45} | {'Code':<10} | {'Grade':<4} | Credits\n"
            output += "-" * 70 + "\n"

            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) == 4:
                    subject = cols[0].text.strip()
                    code = cols[1].text.strip()
                    grade = cols[2].text.strip()
                    credits = cols[3].text.strip()
                    output += f"{subject:<45} | {code:<10} | {grade:<5} | {credits}\n"
        else:
            output += " Grade table not found for this semester.\n"

    output += "\n Fetched first 2 semester results successfully.\n"

except Exception as e:
    output += f"Error: {e}\n"

finally:
    driver.quit()
    print(output)
