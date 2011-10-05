from Frodi.schools.models.schools import School, Preschool, PrimarySchool, SecondarySchool, University, LearningCenter
from country.models.regions import CountryArea
from feedzilla.models import Post
from structure.shortcuts import render

from django.utils.translation import gettext as _
from django.conf import settings

"""
Method that gets all schools of a provided level (supported primary and 
secondary) or all if none is provided in a given region. If no region is
provided the list returned will contain all schools in country. Region is found
using a slug for that region provided. 
"""
def _get_schools(area=None, level=None):
    # Base color of the map
    color = None
    # School level used in the title
    school_level = _('all schools')

    # Get the schools based on school level and store in 'schools' variable
    # We also set map color and school level (which is used in title)
    if level == 'preschool':
        schools = Preschool.objects.all()
        school_level = _('preschools')
        if settings.PRESCHOOL_COLOR:
            color = settings.PRESCHOOL_COLOR
    elif level == 'primary':
        schools = PrimarySchool.objects.all()
        school_level = _('primary schools')
        if settings.PRIMARY_SCHOOL_COLOR:
            color = settings.PRIMARY_SCHOOL_COLOR
    elif level == 'secondary':
        schools = SecondarySchool.objects.all()
        school_level = _('secondary schools')
        if settings.SECONDARY_SCHOOL_COLOR:
            color = settings.SECONDARY_SCHOOL_COLOR
    elif level == 'university':
        schools = University.objects.all()
        school_level = _('universities')
        if settings.UNIVERSITY_COLOR:
            color = settings.UNIVERSITY_COLOR
    elif level == 'learningcenter':
        schools = LearningCenter.objects.all()
        school_level = _('learning centers')
        if settings.LEARNING_CENTER_COLOR:
            color = settings.LEARNING_CENTER_COLOR
    else:
        # Default to all schools
        schools = School.objects.all()

    if area:
        schools = schools.filter(municipality__area=area)

    return (schools, school_level, color)

"""
When rendered the method
also adds a nice map of the country, highlighting the area being looked at.
"""
def list_schools(request, area=None, level=None):
    # Get all areas into a variable (for the map)
    country_areas = CountryArea.objects.all()

    try:
        # Try to get the specific area according to the slug
        country_area = country_areas.get(slug=area)
    except:
	# If we fail, we mark it as none
	country_area = None

    # Get all schools within the given area (or the country if area is None)
    (schools, school_level, color) = _get_schools(country_area, level)

    # Set the title according to the school_level and area
    if country_area:
        title = _(u'%(schools)s in %(area)s') % {'schools':school_level.capitalize(), 'area':country_area.name}
    else:
        title = _(u'All %(schools)s in the country') % {'schools':school_level}

    # Render the template along with a selected area and all areas
    return render('schools/list.html', {'title':title, 'selected_area':country_area, 'areas':country_areas, 'base_color':color, 'schools':schools}, request)

"""
Method that fetches a school (based on a provided slug) and renders it along 
with all country areas (to draw a nice map). The area of the school gets 
highlighted in the template (based on the schools municipality).
"""
def school_info(request, school):
    # Base color of map
    color = None

    # Try to get the school according to the schools slug
    try:
        school = School.objects.get(slug=school)
    except:
        return render('schools/info.html', {}, request)

    # Try to find the school level to set the appropriate color
    # Django does not handle subclasses optimally so this will be ugly and
    # repetitive (I know, I know DRY)

    # Get country areas for the map
    country_areas = CountryArea.objects.all()
    selected_area = school.municipality.area

    try:
        return render('schools/info.html',
                      {'school':school.preschool,
                       'base_color':settings.PRESCHOOL_COLOR,
                       'type':'preschool',
                       'areas':country_areas,
                       'selected_area':selected_area}, request)
    except:
        pass

    try:
        return render('schools/info.html',
                      {'school':school.primaryschool,
                       'base_color':settings.PRIMARY_SCHOOL_COLOR,
                       'type':'primaryschool',
                       'areas':country_areas,
                       'selected_area':selected_area}, request)
    except:
        pass

    try:
        return render('schools/info.html',
                      {'school':school.secondaryschool,
                       'base_color':settings.SECONDARY_SCHOOL_COLOR,
                       'type':'secondaryschool',
                       'areas':country_areas,
                       'selected_area':selected_area}, request)
    except:
        pass

    try:
        return render('schools/info.html',
                      {'school':school.university,
                       'base_color':settings.UNIVERSITY_COLOR,
                       'type':'university',
                       'areas':country_areas,
                       'selected_area':selected_area}, request)
    except:
        pass

    try:
        return render('schools/info.html',
                      {'school':school.learningcenter,
                       'base_color':settings.SECONDARY_SCHOOL_COLOR,
                       'type':'learningcenter',
                       'areas':country_areas,
                       'selected_area':selected_area}, request)
    except:
        pass

    # Render the template with the areas and the school and no particular color
    return render('schools/info.html', {'areas':country_areas, 'selected_area':selected_area, 'school':school}, request)


def list_feeds(request, area=None, level=None):
    try:
        # Try to get the specific area according to the slug
        country_area = CountryArea.objects.get(slug=area)
    except:
	# If we fail, we mark it as none (we're getting all of them)
	country_area = None

    (schools, school_level, color) = _get_schools(area, level)
    posts = Post.objects.filter(feed__schoolinformation__school__in=schools)

    return render('schools/feeds.html', {'school_feeds':posts}, request)
