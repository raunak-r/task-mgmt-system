from django.shortcuts import render
import requests
# Create your views here.
# p/w = raunak. username = raunakritesh.india@gmail.com

def ip(request):
    response = requests.get('http://api.ipstack.com/check?access_key=4151d8748ff647d3da010b4134b97cb0')
    geodata = response.json()
    print(geodata)
    return render(request, 'restapi/ip.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name']
    })