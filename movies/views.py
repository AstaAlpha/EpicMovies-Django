from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os
from decouple import config

AT = Airtable(config('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=config('AIRTABLE_API_KEY'))

def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula = "FIND('" + user_query.lower() + "', LOWER({Name}))")
    result_frontend = {'search_result' : search_result}
    return render(request, 'movies/movies_stuff.html', result_frontend)


def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        
        
        
        try:
            response = AT.insert(data)

            #notification
            messages.success(request, 'New Movie Added: {}'.format(response['fields'].get('Name')))
        
        except Exception as e:
            messages.warning(request, 'Error Creating Movie: {}'.format(e))
        
    return redirect('/')

    

def edit(request, movies_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.update(movies_id, data)

            #notification
            messages.success(request, 'Updated Movie: {}'.format(response['fields'].get('Name')))
            
        except Exception as e:
            messages.warning(request, 'Error Updating Movie: {}'.format(e))
    
    return redirect('/')

def delete(request, movies_id):
    try:
        movies_name = AT.get(movies_id)['fields'].get('Name')
        response = AT.delete(movies_id)

        #notification
        messages.warning(request, 'Movie Deleted: {}'.format(movies_name))
        
    except Exception as e:
        messages.warning(request, 'Error Deleting Movie {}'.format(e))

    return redirect('/')