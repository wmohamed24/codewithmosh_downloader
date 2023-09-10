from getCoursesClass import getCoursesClass
import os
from pathlib import Path


def get_downloads_path():
    platform_system = os.name
    home = Path.home()

    if platform_system == "nt":  # For Windows
        return os.path.join(home, "Downloads")
    elif platform_system == "posix":  # For macOS and Linux
        return os.path.join(home, "Downloads")
    else:
        raise NotImplementedError(f"Unsupported OS: {platform_system}")
    

def main():
    download_path = get_downloads_path()
    course_path = os.path.join(os.curdir, "Courses")
    if not os.path.exists(course_path):
        os.mkdir(course_path)

    get_courses: getCoursesClass = getCoursesClass("127.0.0.1:9222", download_path, course_path)
    
    # course_link = "https://members.codewithmosh.com/courses/1120640/lectures/24393589"
    # check_link = "https://members.codewithmosh.com/courses/1120640/lectures/"
    # get_courses.get_course_all("Git", course_link, check_link)

    get_courses.login()
    


if __name__ == "__main__":
    main()
