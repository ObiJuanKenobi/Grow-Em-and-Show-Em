from pga.dataAccess import DataAccess

#Retrieves all courses and adds them to the data dictionary passed in,
# which is returned by each view
def add_courses_to_dict(dict):
    db = DataAccess()
    courses = db.getCourses()
    #dict['courses'] = courses
    
    colors = []
    for course in courses:
        colors.append(db.getCourseColor(course['Course_Name']))
    #dict['colors'] = colors
    dict['courses'] = zip(courses, colors)
    return dict;
    
#Sets color and name for home page & login/logout views
def get_home_page_dict():
    return {'course': 'Gardening 101', 'color': '01af01'}