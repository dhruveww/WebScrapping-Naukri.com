from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url = "https://www.naukri.com/"
s = Service("C:/Users/SURESH PATEL/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get(url)

# Wait until the search input box is present
searchjob = input("Enter any skill/designation/company: ")
searchjobbutton = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, """/html/body/div[1]/div[7]/div/div/div[1]/div/div/div/div[1]/div/input"""))
)
searchjobbutton.send_keys(searchjob)

yn = input("If you want to enter the location, enter 'y' for yes and 'n' for no: ")
locationbutton = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, """/html/body/div[1]/div[7]/div/div/div[5]/div/div/div/div[1]/div/input"""))
)
if yn == 'y':
    place = input("Enter the location: ")
    locationbutton.send_keys(place)
    more = input("Do You want to enter multiple locations type 'y', if not type 'n'")
    if more == 'n':
        enterbutton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, """/html/body/div[1]/div[7]/div/div[1]/div[6]""")))
        enterbutton.click()
    while more == 'y':
        moreplace = input("enter the location: ")
        locationbutton.send_keys(f',{moreplace}')
        more = input("Do You want to enter one more location type 'y', if not type 'n'")
        if more == 'n':
            enterbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div[1]/div[7]/div/div[1]/div[6]""")))
            enterbutton.click()
            break
else:
    enterbutton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, """/html/body/div[1]/div[7]/div/div[1]/div[6]""")))
    enterbutton.click()


job_titles = []
companies = []
reviews=[]
ratings=[]
location=[]
salary=[]
experience = []
posting_date=[]  
job_urls = []
openings  = []
applicants  = []

#WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "srp-jobtuple-wrapper")))
#currentpageurl = driver.current_url
#questionindex = currentpageurl.index('?')
   
#next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div/div/main/div[1]/div[2]/div[3]/div/a[2]""")))
#next_button.click()
for page in range(1,3):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
    )
    time.sleep(3)
    print(f"Scraping page {page}: {driver.current_url}")
    #print(driver.current_url)
    # Wait until the job listings are present
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "srp-jobtuple-wrapper")))
    
    soup = bs(driver.page_source, 'html.parser')
    jobs = soup.find_all('div', class_="srp-jobtuple-wrapper")
    
    
    # Loop through all job elements and extract the title
    for job in jobs:
        title_element = job.find('a', class_='title')
        title_url = title_element.attrs['href']
        if title_element:
            job_titles.append(title_element.get_text().strip())
            job_urls.append(title_url)
        else:
            job_titles.append("null")
            job_urls.append("null")
            
        
        company_name = job.find('a',class_="comp-name")
        if company_name:
            companies.append(company_name.get_text().strip())
        else:
            companies.append("null")
        #review = job.find('a',class_=" review ver-line")
        #if review:
        #    reviews.append(review.get_text().strip())
        #else:
        #    reviews.append("null")
        #reviews_element = job.find('a', class_='review ver-line')
        #if reviews_element:
        #    reviews = driver.execute_script("return arguments[0].innerText;", reviews_element).strip()
        #else:
        #    reviews = 'N/A'
        #reviews_element_xpath = f"(//div[@class='srp-jobtuple-wrapper']//a[@class='review ver-line'])[{index + 1}]"
        #try:
        #    reviews_element = WebDriverWait(driver, 10).until(
        #        EC.presence_of_element_located((By.XPATH, reviews_element_xpath))
        #    )
        #    reviews = reviews_element.text.strip()
        #except:
        #    reviews = 'N/A'
        rating = job.find('span',class_="main-2")
        if rating:
            ratings.append(rating.get_text().strip())
        else:
            ratings.append("null")
        exp = job.find('span',class_="expwdth")
        if exp:
            experience.append(exp.get_text().strip())
        else:
            experience.append("null")
        pay = job.find('span',class_='', title=True)
        if pay:
            salary.append(pay.get_text().strip())
        else:
            salary.append("null")
        loc = job.find('span',class_="")
        if loc:
            location.append(loc.get_text().strip())
        else:
            location.append("null")
        posted = job.find('span',class_="job-post-day")
        if posted:
            posting_date.append(posted.get_text().strip())
        else:
            posting_date.append("null")
    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div/div/main/div[1]/div[2]/div[3]/div/a[2]""")))
        next_button.click()
    except Exception as e:
        time.sleep(3)
        print(f"No more pages to scrape. Scraped {page} pages.")
        break



for joburl in job_urls:
    driver.get(joburl)
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"""/html/body/div/div/main/div[1]/div[1]/section[1]""")))
    soup = bs(driver.page_source,'html.parser')
    opening = soup.find_all('span',class_="styles_jhc__stat__PgY67")[1]
    openings.append(opening.get_text().strip() if opening else "null")
    applicant = soup.find_all('span',class_="styles_jhc__stat__PgY67")[2]
    applicants.append(applicant.get_text().strip() if applicant else "null")
    driver.quit()
        
df = pd.DataFrame({"title":job_titles,"company name":companies,"location":location,"salary":salary,"posted at":posting_date,"experience level": experience,"ratings":ratings,"openings":openings,"applicants":applicants})
df.to_excel('new6.xlsx', index=True)
#print("companies:")
#for comp in reviews:
#    print(comp)

# Close the browser
#driver.quit()
