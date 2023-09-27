
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import datetime
import shutil


class getCoursesClass:

    def __init__(self, debugger_address, download_path, course_path):
        self.debugger_address = debugger_address
        options = webdriver.ChromeOptions()
        options.debugger_address = debugger_address
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.download_path = download_path
        self.courses_path = course_path

    def check_element_exists(self, by, value):
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def download_course(self):
        previous_download = None
        while (True):
            current_url = self.driver.current_url
            pattern = re.compile('lecture')

            if not pattern.search(current_url):
                break

            if self.check_element_exists(By.XPATH, '//a[@aria-label="Download this video"]'):
                download_button = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//a[@aria-label="Download this video"]')))
                download_button.click()

            next_btn = self.wait.until(EC.presence_of_element_located(
                (By.ID, 'lecture_content_complete_button')))
            
            if previous_download != None and previous_download == next_btn:
                break
            
            if (previous_download == None):
                previous_download = next_btn

            next_btn.click()
            time.sleep(3)

    def gather_course(self, course_name):
        today = datetime.date.today()
        files_today = []

        files = [f for f in os.listdir(self.download_path) if os.path.isfile(
            os.path.join(self.download_path, f)) and f.endswith('.mp4')]

        for filename in files:
            file_date = datetime.date.fromtimestamp(
                os.path.getctime(os.path.join(self.download_path, filename)))
            if file_date == today:
                files_today.append(filename)

        course_folder = f"{self.download_path}/{course_name}"

        # Create the new folder if it doesn't exist
        if not os.path.exists(course_folder):
            os.makedirs(course_folder)

        for file_name in files_today:
            source_path = os.path.join(self.download_path, file_name)
            destination_path = os.path.join(course_folder, file_name)

            shutil.move(source_path, destination_path)

    def rename_course_vids(self, course_name):

        folder_path = f"{self.download_path}/{course_name}"
        files = [f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f))]

        # Sort the files based on their creation time
        files_sorted = sorted(files, key=lambda x: os.path.getctime(
            os.path.join(folder_path, x)))

        # Rename the files
        for idx, filename in enumerate(files_sorted, start=1):
            ext = os.path.splitext(filename)[1]
            new_name = f"{course_name}_{idx}{ext}"
            os.rename(os.path.join(folder_path, filename),
                      os.path.join(folder_path, new_name))

    def zip_course(self, course_name):
        output_path = f"{self.courses_path}/{course_name}"
        folder_path = f"{self.download_path}/{course_name}"

        shutil.make_archive(output_path, 'zip', folder_path)

        shutil.rmtree(folder_path)

    def get_course_all(self, course_name, ):
        self.download_course()
        self.gather_course(course_name)
        self.rename_course_vids(course_name)
        self.zip_course(course_name)

    def get_course_list(self):
        self.driver.get('https://members.codewithmosh.com/courses/enrolled')
        course_ids = list()
        course_titles = list()
        while (True):

            ids = self.driver.find_elements(By.CSS_SELECTOR, '.course-listing')
            course_ids += [id.get_attribute('data-course-id') for id in ids]

            titles = self.driver.find_elements(By.CSS_SELECTOR, '.course-listing-title')
            course_titles += [title.text.replace(" ", "_").replace(":", "") for title in titles]

            if self.check_element_exists(By.CSS_SELECTOR, '.next'):
                next_btn = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.next')))
                next_btn.click()
                time.sleep(5)
            else:
                break
        return course_ids, course_titles
    

    
    def login(self):
        pattern = re.compile(r'^https://members.codewithmosh.com/')

        if pattern.search(self.driver.current_url):
            return

        self.driver.get("https://sso.teachable.com/secure/146684/identity/login/password")
        
        email_elem = self.driver.find_element(By.ID, 'email')  
        password_elem = self.driver.find_element(By.ID, 'password')  
        login_btn = self.driver.find_element(By.XPATH, "//input[@value='Log in']")

        
        email_elem.send_keys('email')
        password_elem.send_keys('password')

        login_btn.click()

    def get_course_entry(self, id):
        
        self.driver.get(f'https://members.codewithmosh.com/courses/enrolled/{id}')
        time.sleep(1)

        if self.check_element_exists(By.XPATH, "//ul[@class='section-list'][1]/li[1]/a[1]"):
            first_vid = self.driver.find_element(By.XPATH, "//ul[@class='section-list'][1]/li[1]/a[1]")
            first_vid.click()
        elif self.check_element_exists(By.XPATH, '//*[@id="__next"]/div/div/div[3]/div[1]/div[2]/div[2]/div[1]/a[1]'):
            first_vid = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/a[1]')
            first_vid.click()

        else:
            return
        