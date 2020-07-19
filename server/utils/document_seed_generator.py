from faker import Faker
from faker.providers import internet, address, date_time, geo, person, phone_number
from datetime import datetime
from logging import Logger
import json


'''
Facilitates conveniently generating random JSON documents for DB seeding using the faker library
add several randomly generated key:value pairs to a seeder object and then use it anywhere
'''
class Seeder():
    def __init__(self):
        fake = Faker()
        #add several providers for convenience
        fake.add_provider(internet)
        fake.add_provider(address)
        fake.add_provider(date_time)
        fake.add_provider(geo)
        fake.add_provider(person)
        fake.add_provider(phone_number)
        self.faker = fake
        Faker.seed(datetime.now())
    
    def add_randomizer(self, keyname = None, randomizerfunc = lambda x: None, gen_dict = {}):
        '''
        adds a randomly generated datatype to the JSON document being generated by Seeder  
        in the format "keyname" : lambda x: faker.randomizerfunc(faker) 
        if there is already a generation function in the dictionary, it will be overwritten
        Parameters: 
            keyname(string):                                        the name of the JSON key
            randomizerfunc:(function(faker) -> Object(JSONEncoder))      the function responsible for randomly generating 
                                                                        this key's value which must be JSON encodable
                                                                        NOTE: the randomizerfunc must take a faker as an argument
                                                                        to inject this dependency
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Returns:
            None
        '''
        gen_dict[keyname] = randomizerfunc

    def gen_rand_dict(self, gen_dict = {}) -> 'Document':
        '''
        randomly generates one dictionary record with the current JSON in this object's gendict
        Parameters: 
            seed(Primitive): data used to seed the Random.random instance of the faker
                NOTE: do not change this for any purpose other than testing, set to 0 for tests so that the outputs are identical
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Returns: 
            JSONDoc(dict): a dictionary of the format key:value generated
        '''
        Document = {}
        #The key value tuples are in the form "property" : randomizationfunc(faker)
        #loop through all of the generation functions and generate the random values
        for Keyval in gen_dict.items():
            Document[Keyval[0]] = Keyval[1](self.faker)
            #Keyval[1] is a function, adding (self.faker) next to it calls that function returning the random value from faker
        return Document

    def clean(self, gen_dict = {}) -> 'Cleaned Keys':
        '''
        removes the invalid random generation functions from the current generation dictionary
        Params: 
            gen_dict({string: function(faker)}): the dictionary of functions for random generation
        Return: 
            None
        '''
        cleaned_keys = []
        for Keyval in gen_dict.items():
            try:
                #this will try to encode each value as json
                json.dumps(Keyval[1](self.faker))
            except:
                #if any exception occurs while trying to encode the values, then that function is marked for removal
                print(f"[ {Keyval[0]} ]: invalid random generation function, cleaning...")
                cleaned_keys.append(Keyval[0])
        #remove the functions in a separate loop since dict.items() is not modification safe
        for Key in cleaned_keys:
            gen_dict.pop(Key, None)
        return cleaned_keys #return the list of values that had invalid randomization functions
    
'''
several utility randomization functions
'''

#randomly generates a restaurant name in format "{name}'s {dish}s"
def restaurant_name_randomizer(faker, dish_dict):
    return faker.name() + "'s " + faker.random_element(dish_dict) + "s"

#randomly generates a phone number accounting for faker's default format
def valid_phone_number(faker):
    return "".join(filter(str.isdigit,faker.phone_number().split('x')[0]))
    #generates a random integer representing a phone number, the faker format is "+(country code) pho-nen-umberxExtension"
    #so it is necessary to split the end off past 'x' and only accept numeric characters
    