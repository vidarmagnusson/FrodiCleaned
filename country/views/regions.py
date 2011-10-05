from country.models.regions import CountryArea
from structure.shortcuts import render

"""
A simple method which draws all areas in a country. Uses the country/areas.html
template (the method should actually be a method in a country view. The method
has an optional parameter 'color' which is used in the rendering as the base
color of the country. The default color is a soft brown (for no particular
reason, but it's a nice colour though).
"""
def list_areas(request, color=None):
    return render('country/areas.html', {'areas':CountryArea.objects.all(), 'scale_map':2, 'base_color':color}, request)
