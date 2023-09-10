from getCoursesClass import getCoursesClass


def main():
    get_courses: getCoursesClass = getCoursesClass("127.0.0.1:9222")
    course_link = "https://members.codewithmosh.com/courses/293204/lectures/4509750"
    check_link = "https://members.codewithmosh.com/courses/293204/lectures"
    get_courses.get_course_all("NodeJS", course_link, check_link)


if __name__ == "__main__":
    main()
