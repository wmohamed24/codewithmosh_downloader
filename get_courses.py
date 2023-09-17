from getCoursesClass import getCoursesClass
import os
from pathlib import Path
from selenium import webdriver
import time


def get_to_login():

    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=options)
    driver.get("https://sso.teachable.com/secure/146684/identity/login/password")
    driver.quit()



def get_downloads_path():
    platform_system = os.name
    home = Path.home()

    if platform_system == "nt":  # For Windows
        return os.path.join(home, "Downloads")
    elif platform_system == "posix":  # For macOS and Linux
        return os.path.join(home, "Downloads")
    else:
        raise NotImplementedError(f"Unsupported OS: {platform_system}")
    
def download_courses(get_courses:getCoursesClass, id_title_map):
    
    for id, title in id_title_map.items():
        print(id, title)
        get_courses.get_course_entry(id)
        time.sleep(1)
        get_courses.get_course_all(title)




    
    

def main():
    download_path = get_downloads_path()
    course_path = os.path.join(os.curdir, "Courses")
    if not os.path.exists(course_path):
        os.mkdir(course_path)

    get_to_login()
    time.sleep(3)

    get_courses: getCoursesClass = getCoursesClass("127.0.0.1:9222", download_path, course_path)
    get_courses.login()

    course_ids, course_titles = get_courses.get_course_list()
    if 'Complete_Python_Mastery' in course_titles:
        course_ids, course_titles = course_ids[1:], course_titles[1:]

    id_title_map = dict(zip(course_ids, course_titles))
    id_title_map.pop("417695", None)
    id_title_map.pop("525068", None)
    id_title_map.pop("2037633", None)
    id_title_map.pop("2178940", None)
    id_title_map.pop("2037633", None)
    id_title_map.pop("2074069", None)
    id_title_map.pop("1779784", None)


    #to download all
    download_courses(get_courses, id_title_map)


    # ids_to_download = ['1779784']
    # titles_to_download = [id_title_map[key] for key in ids_to_download if key in id_title_map]

    # download_courses(get_courses, ids_to_download, titles_to_download)

    #"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="E:\git\codewithmosh_downloader\ChromeSession"



    
    


if __name__ == "__main__":
    main()
