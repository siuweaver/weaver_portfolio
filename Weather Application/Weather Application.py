# DSC 510
# Week 12
# Programming Assignment Week 12
# Author Ryan Weaver
# 11/13/2022

import requests
import re


def get_type_input():
    print('In order to proceed, you need to specify input type: ')
    type_input = input('To enter a US zipcode press 1, To enter a city press 2, or Q to quit: ')
    type_input_loop = 1
    while type_input_loop == 1:
        if type_input == '1':
            type_input_loop = 0
        elif type_input == '2':
            type_input_loop = 0
        elif type_input.lower() == 'q':
            type_input_loop = 0
        else:
            print('Only input 1, 2, or Q')
            type_input = input('To enter a US zipcode press 1, To enter a city press 2, or Q to quit: ')
    return type_input


def zip_code_format(zip_code_input):
    zip_code_format_loop = 1
    while zip_code_format_loop == 1:
        # testing for 9 continuous numbers
        if re.match(r"^\d{9}$", zip_code_input):
            zip_code_output = zip_code_input[:5]
            zip_code_format_loop = 0
        # testing for 5 numbers that end with a hyphen
        elif re.match(r"^\d{5}-$", zip_code_input):
            zip_code_output = zip_code_input[:5]
            zip_code_format_loop = 0
        # testing for 5 numbers, hyphen, then 4 numbers
        elif re.match(r"^\d{5}-\d{4}$", zip_code_input):
            zip_code_output = zip_code_input[:5]
            zip_code_format_loop = 0
        # testing for 5 continuous numbers
        elif re.match(r"^\d{5}$", zip_code_input):
            zip_code_format_loop = 0
            zip_code_output = zip_code_input
        else:
            zip_code_input = input('Please enter a US zip code, example 68104: ')
    return zip_code_output


def get_geocode_from_zip(api_key_id):
    zip_code_loop = 1
    zip_country_code = 'US'
    zip_code = input('Enter a US zip code: ')
    while zip_code_loop == 1:
        zip_code = zip_code_format(zip_code)
        zip_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{zip_country_code}&appid={api_key_id}"
        if requests.get(zip_url).status_code == 200:
            geocode_zip_response = requests.get(zip_url).json()
            if len(geocode_zip_response) > 0:
                zip_code_loop = 0
            else:
                zip_code_loop = 1
                zip_code = input('Zip code was not found, please try again: ')
                zip_code = zip_code_format(zip_code)
        else:
            zip_code = input('Zip code was not found, please try again: ')
            zip_code = zip_code_format(zip_code)
    zip_location_input = [geocode_zip_response['lat'], geocode_zip_response['lon']]
    return zip_location_input


def get_geocode_from_city(api_key_id):
    limit_geocode = 10
    city_loop = 1
    city_name = input('Enter city name: ')
    while city_loop == 1:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit_geocode}&appid={api_key_id}"
        if requests.get(url).status_code == 200:
            geocode_city_response = requests.get(url).json()
            if len(geocode_city_response) > 0:
                city_loop = 0
            else:
                city_loop = 1
                city_name = input('City name was not found, please try again: ')
        else:
            print('There was an error retrieving the geocode')
    return geocode_city_response


def get_country(geocode_city_response):
    country_input = ''
    list_of_countries = []
    for line in geocode_city_response:
        country_line = line['country']
        if country_line not in list_of_countries:
            list_of_countries.append(country_line)
    # if only one country is returned, choose automatically
    if len(list_of_countries) == 1:
        print('Your selected Country is ' + list_of_countries[0])
        country_input = list_of_countries[0]
        return country_input
    elif len(list_of_countries) > 1:
        country_input_loop = 1
        while country_input_loop == 1:
            print('Please choose from the following list: ')
            # returns list of countries for the user to select
            for country_list_item in list_of_countries:
                print(country_list_item)
            country_input = str(input('enter: '))
            country_input = country_input.upper()
            if country_input not in list_of_countries:
                country_input_loop = 1
            else:
                country_input_loop = 0
    else:
        print('get_country else statement')
    return country_input


def get_state(geocode_city_response, country_code):
    list_of_states = []
    if country_code != 'US':
        state_code = ''
    # Only return a state if the country is the US
    else:
        for line in geocode_city_response:
            state_line = line['state']
            # Only return states in the US
            if line['country'] == country_code:
                if state_line not in list_of_states:
                    list_of_states.append(state_line)
        # if only one state is returned, choose automatically
        if len(list_of_states) == 1:
            print('Your selected State is ' + list_of_states[0])
            state_code = list_of_states[0]
        elif len(list_of_states) > 1:
            state_input_loop = 1
            while state_input_loop == 1:
                print('Please choose from the following list: ')
                # returns a list of states for the user to choose from
                for state_list_item in list_of_states:
                    print(state_list_item)
                get_state_input = str(input('enter: '))
                if get_state_input.title() not in list_of_states:
                    state_input_loop = 1
                else:
                    state_input_loop = 0
                    state_code = get_state_input.title()
        else:
            print('get_state else statement')
    return state_code


def filter_city_api_response(api_key):
    # retrieves a list of cities that match input
    api_city_response_list = get_geocode_from_city(api_key)
    # retrieves the country inputted by the user to filter the list
    country_input = get_country(api_city_response_list)
    # retrieves the state inputted by the user to filter the list
    state_input = get_state(api_city_response_list, country_input)
    state_line = ''
    filtered_city_list = []
    for line in api_city_response_list:
        country_line = line['country']
        # records outside US may not have a state
        try:
            state_line = line['state']
        except KeyError:
            pass
        else:
            state_line = line['state']
        if country_line == country_input:
            if country_input == 'US':
                if state_input == state_line:
                    filtered_city_list.append(line)
            else:
                filtered_city_list.append(line)
    city_location_input = filtered_city_list[0]['lat'], filtered_city_list[0]['lon']
    return city_location_input


def get_unit_of_measurement():
    print('What unit of measurement would you like see? ')
    unit_of_measurement = input('Press 1 for Fahrenheit, Press 2 for Celsius, Press 3 for Kelvin: ')
    get_unit_loop = 1
    while get_unit_loop == 1:
        if unit_of_measurement == '1':
            unit_value = 'imperial'
            get_unit_loop = 0
        elif unit_of_measurement == '2':
            unit_value = 'metric'
            get_unit_loop = 0
        elif unit_of_measurement == '3':
            unit_value = 'standard'
            get_unit_loop = 0
        else:
            print('Only enter 1,2, or 3')
            unit_of_measurement = input('Press 1 for Fahrenheit, Press 2 for Celsius, Press 3 for Kelvin: ')
    return unit_value


def get_weather(location_list, unit, api_key_id):
    location_lat = location_list[0]
    location_lon = location_list[1]
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location_lat}&lon={location_lon}&appid={api_key_id}&units={unit}"
    if requests.get(open_weather_url).status_code == 200:
        open_weather_response = requests.get(open_weather_url).json()
        print("Today's low is " + str(open_weather_response['main']['temp_min']) + ' degrees.')
        print("Today's high is " + str(open_weather_response['main']['temp_max']) + ' degrees.')
        print("The current temperature is " + str(open_weather_response['main']['temp']) + ' degrees.')
        print("The feels like temperature is " + str(open_weather_response['main']['feels_like']) + ' degrees.')
    else:
        print('An error occurred trying to retrieve weather')


def main():
    api_key = '89f04e31fb68cfc4f1f2c1dfc11514a5'
    print('Welcome to my weather app!')
    continue_loop = 1
    # get whether the user wants to enter zip code, city, or quit
    continue_type = get_type_input()
    if continue_type == 'q':
        continue_loop = 0
    while continue_loop == 1:
        if continue_type == '1':
            # get the lat/lon based on the zip code entered
            location_input = get_geocode_from_zip(api_key)
        elif continue_type == '2':
            # get the lat/lon based on the zip, state, and country entered
            location_input = filter_city_api_response(api_key)
        # retrieves whether the user wants to see in Fahrenheit, Celsius, or Kelvin
        unit = get_unit_of_measurement()
        # api call to get the weather based on the lat/lon
        get_weather(location_input, unit, api_key)
        # get whether the user wants to enter zip code, city, or quit
        continue_type = get_type_input()
        if continue_type == 'q':
            continue_loop = 0
    print('Thanks for using my app!')


if __name__ == '__main__':
    main()
