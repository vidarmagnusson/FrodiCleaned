# -*- coding: utf-8 -*-
from structure.shortcuts import render

def social(request):
        return render('social.html', {}, request)

def tags(request,tag):
	return render('social.html', {}, request)
