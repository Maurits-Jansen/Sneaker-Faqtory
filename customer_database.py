import numpy as np
import pandas as pd
import os

# Import the functions
from customer_functions import *

# Fake dataset from www.fakenamegenerator.com
dfs=[]
for i in range(0,6):
    filename = '/GeneratorData/FakeNameGeneratorData' + str(i) + '.txt'
    if i == 1: sep='\t'
    else: sep='|'
    df = pd.read_csv(os.getcwd() + '/Customers/' + filename, sep=sep)
    dfs.append(df)
data = pd.concat(dfs, axis=0, ignore_index=True)

#Remove duplicates
data = data.drop_duplicates()
print(data.shape)

# The location of the flagship stores (capitals)
stores_latlon = {'Netherlands': [52.3676,4.9041],
                 'Belgium': [52.3676,4.9041],    #maps to Amsterdam/Netherlands
                 'United Kingdom': [51.5072, 0.1276],
                 'Sweden': [59.3293, 18.0686],
                 'Spain': [40.4168, 3.7038],
                 'Poland': [52.2297, 21.0122],
                 'Italy': [41.9028, 12.4964]}

# The weights per country (arbitrary)
country_share = {'Netherlands': 0.8*0.34,
                 'Belgium': 0.2*0.34,
                 'United Kingdom': 0.25,
                 'Sweden': 0.083,
                 'Spain': 0.166,
                 'Poland': 0.0415,
                 'Italy': 0.125}

# Take a sample of the input data with the distance from stores weights
# And the country weights
customer_data = country_sample(capital_sample(data, stores_latlon), country_share)

# Remove additional columns
customer_data = customer_data[['Gender', 'GivenName', 'Surname', 'StreetAddress',
                                'City', 'ZipCode', 'Country', 'CountryFull',
                                'EmailAddress', 'TelephoneNumber', 'TelephoneCountryCode',
                                'Birthday', 'Age', 'Latitude', 'Longitude']]
print(customer_data.shape)

# Add customerID
customer_data.insert(0, 'customerID', ['C'+str(i) for i in range(int(1e5), int(1e5) + len(customer_data))])

# Write to file
customer_data.to_csv(os.getcwd() + '/Customers/customer_database.txt', sep='\t', index=False)
