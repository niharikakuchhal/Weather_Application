"""
    Weather Module
    
    Functions
    
        get_lat_lon(city)
            return lattitude and longitude of given city or False if city not availaable
            
        get_temp(lat,lon)
            return temprature dict or empty dictionary if city data not available
            temprature dict = {
                        'data':data,
                        'name':name,
                        'temp':temp,
                        'desc':desc,
                        'icon':f"https://openweathermap.org/img/wn/{icon}@4x.png"
                    }
            
"""
import requests
import os

def get_lat_lon(city):  
    """ 
    return lattitude and longitude of given city or False if city not availaable
    """
    city = city.strip().lower()
    url = "https://api.openweathermap.org/data/2.5/weather"
    param = {
        'q':city,
        'appid':"09cfa4fdecdd68829518e0168f1f023b"
    }
    resp = requests.get(url,param)
    if resp.status_code == 200:
        try:
            ans = resp.json()['coord']
            lat = ans['lat']
            lon = ans['lon']
            return lat,lon
        except:
            return False
    return False


def get_temp(lat,lon): 
    """ return temprature dict or empty dictionary if city data not available
            temprature dict = {
                        'data':data,
                        'name':name,
                        'temp':temp,
                        'desc':desc,
                        'icon':f"https://openweathermap.org/img/wn/{icon}@4x.png"
                    }
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    param = {
        'lat': lat,
        'lon': lon,
        'units':'metric',
        'appid':"09cfa4fdecdd68829518e0168f1f023b"

    }
    resp = requests.get(url,param)
    if resp.status_code == 200:
        try:
            data = resp.json()
            name = data['name']
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            return {
                'name':name,
                'temp':temp,
                'desc':desc,
                'icon':f"https://openweathermap.org/img/wn/{icon}@4x.png"
            }
        
        except Exception as e:
            print("Error!",e)
            return {}
    else:
        print('\nSomething went wrong')
        print(f'Status Code : {resp.status_code} {resp.reason}')
        return {}
    
if __name__ == '__main__':
    os.system('cls')
    print('\n\n\n')
    city = input('Enter City Name: '.rjust(50))
    coord = get_lat_lon(city)
    if coord:
        lat,lon = coord
        data = get_temp(lat,lon)
        for k,v in data.items():
            print(f"{k:>30} = {v}")
        print('\n\n\n')
    else:
        print('City not found')
