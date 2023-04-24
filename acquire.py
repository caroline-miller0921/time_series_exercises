import requests

import numpy as np
import pandas as pd
import os

import math


# acquire the full people dataframe
def acquire_swapi_people():
    
    if os.path.isfile('swapi_people.csv'):
        return pd.read_csv('swapi_people.csv')
    
    else:
        
        response = requests.get('https://swapi.dev/api/people/')

        data = response.json()
        data.keys()
            
        number_of_people = data['count']
        next_page = data['next']
        previous_page = data['previous']

        print(f'number_of_people: {number_of_people}')
        print(f'next_page: {next_page}')
        print(f'previous_page: {previous_page}')

        number_of_results = len(data['results'])
        max_page = math.ceil(number_of_people / number_of_results)

        print(f'number_of_results: {number_of_results}')
        print(f'max_page: {max_page}')

        people_df = pd.DataFrame(data['results'])
        
        for i in range (2, (max_page + 1)):
            
            response = requests.get(f'https://swapi.dev/api/people/?page={i}')
            print({i})
            data = response.json()
            people_df = pd.concat([people_df, pd.DataFrame(data['results'])], axis=0, ignore_index=True)

        people_df.to_csv('swapi_people.csv')
            
        return people_df
    
# acquire full planets dataframe    
def acquire_swapi_planets():
    
    if os.path.isfile('swapi_planets.csv'):
        return pd.read_csv('swapi_planets.csv')
    
    else:
        
        response = requests.get('https://swapi.dev/api/planets/')

        data = response.json()
        data.keys()
            
        number_of_planets = data['count']
        next_page = data['next']
        previous_page = data['previous']

        print(f'number_of_planets: {number_of_planets}')
        print(f'next_page: {next_page}')
        print(f'previous_page: {previous_page}')

        number_of_results = len(data['results'])
        max_page = math.ceil(number_of_planets / number_of_results)

        print(f'number_of_results: {number_of_results}')
        print(f'max_page: {max_page}')

        planets_df = pd.DataFrame(data['results'])
        
        for i in range (2, (max_page + 1)):
            
            response = requests.get(f'https://swapi.dev/api/planets/?page={i}')
            print({i})
            data = response.json()
            planets_df = pd.concat([planets_df, pd.DataFrame(data['results'])], axis=0, ignore_index=True)

        planets_df.to_csv('swapi_planets.csv')
            
        return planets_df
    
# acquire full starships dataframe

def acquire_swapi_starships():
    
    if os.path.isfile('swapi_starships.csv'):
        return pd.read_csv('swapi_starships.csv')
    
    else:
        
        response = requests.get('https://swapi.dev/api/starships/')

        data = response.json()
        data.keys()
            
        number_of_starships = data['count']
        next_page = data['next']
        previous_page = data['previous']

        print(f'number_of_starships: {number_of_starships}')
        print(f'next_page: {next_page}')
        print(f'previous_page: {previous_page}')

        number_of_results = len(data['results'])
        max_page = math.ceil(number_of_starships / number_of_results)

        print(f'number_of_results: {number_of_results}')
        print(f'max_page: {max_page}')

        starships_df = pd.DataFrame(data['results'])
        
        for i in range (2, (max_page + 1)):
            
            response = requests.get(f'https://swapi.dev/api/starships/?page={i}')
            print({i})
            data = response.json()
            starships_df = pd.concat([starships_df, pd.DataFrame(data['results'])], axis=0, ignore_index=True)

        starships_df.to_csv('swapi_starships.csv')
            
        return starships_df
    
# Merge poeople, planets, and starships dataframes

def starwars_merge():

    people_df = acquire_swapi_people()
    starships_df = acquire_swapi_starships()
    planets_df = acquire_swapi_planets()

    people_and_ships = pd.merge(left=people_df.explode('starships'),
                            right=starships_df,
                            left_on='starships',
                            right_on='url',
                            how='left',
                            suffixes=['_people', '_starships'])
    
    starwars_df = pd.merge(left=people_and_ships,
         right=planets_df,
         how='left',
         left_on='homeworld',
         right_on='url')
    
    starwars_df = starwars_df.drop(columns={'Unnamed: 0_people', 'Unnamed: 0_starships', 'Unnamed: 0'})

    return starwars_df