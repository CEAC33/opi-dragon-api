import os
import copy
from pymongo import MongoClient
from sanic.log import logger
from config import *
from bson.objectid import ObjectId

from collections import OrderedDict



class MongoUtils:

    def __init__(self):
        MONGO_HOST = os.environ.get('MONGO_HOST')
        MONGO_PORT = int(os.environ.get('MONGO_PORT'))
        MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        MONGO_DB = os.environ.get('MONGO_DB')
        MONGO_USER = os.environ.get('MONGO_USER')
        MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        MONGO_MECHANISM = os.environ.get('MONGO_MECHANISM')
        MONGO_DB_ENV = os.environ.get('MONGO_DB_ENV')

        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        
        if MONGO_PASSWORD:
            self.client[MONGO_DB].authenticate(MONGO_USER, MONGO_PASSWORD, mechanism=MONGO_MECHANISM)
        self.db=self.client[MONGO_DB_ENV]

    # async def save_to_mongo(config, data, collection):
    #     client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
    #     if config.MONGO_PASSWORD:
    #         client[config.MONGO_DB].authenticate(config.MONGO_USER, config.MONGO_PASSWORD, mechanism=config.MONGO_MECHANISM)
    #     db=client[config.MONGO_DB]

    #     my_collection = db[collection]
    #     my_collection_id = my_collection.insert_one(data).inserted_id
    #     return str(my_collection_id)

    def get_from_mongo(self, collection, key_match, value_match):
        result = []
        
        my_collection = self.db[collection]

        if key_match == '_id':
            for x in my_collection.find({ key_match : ObjectId(value_match)}):
                result.append(x)

            result[key_match] = str(result[key_match])
        else:
            for x in my_collection.find({ key_match : value_match}):
                x["id"] = str(x.pop("_id"))
                x["updated_at"] = str(x.pop("updated_at"))
                result.append(x)

        return result

    def get_count_from_mongo(self, collection):        
        my_collection = self.db[collection]
        count = my_collection.count()
        return count

    def get_from_mongo_by_range(self, collection, key_match, start_range, end_range):
        result = []
        
        my_collection = self.db[collection]

        for x in my_collection.find({ key_match : { "$gt": start_range, "$lt": end_range } }):
            x["id"] = str(x.pop("_id"))
            x["updated_at"] = str(x.pop("updated_at"))
            result.append(x)

        return result

    def get_from_mongo_like(self, collection, key_match, word_like):
        result = []
        
        my_collection = self.db[collection]

        for x in my_collection.find({ key_match : {'$regex': word_like, '$options': 'i'}}):
            x["id"] = str(x.pop("_id"))
            x["updated_at"] = str(x.pop("updated_at"))
            result.append(x)

        return result

    def get_unique_from_mongo(self, collection, distinct_field):
        result = []
        
        my_collection = self.db[collection]

        for x in my_collection.distinct(distinct_field):
            result.append(x)

        return result

    def search_in_mongo(self, text, price_range, model, location, year, mileage_range, brand, fuel_type, page_size=20, page_number=1):
        results = {}
        
        my_collection = self.db['cars']

        if text != "" and text != None:
            for x in my_collection.find({'$or': [
                { 'title' : {'$regex': text, '$options': 'i'}},
                { 'description' : {'$regex': text, '$options': 'i'}}
                ]}):
                x["id"] = str(x.pop("_id"))
                x["updated_at"] = str(x.pop("updated_at"))
                results[x["id"]] = x
        else:
            for x in my_collection.find({}):
                x["id"] = str(x.pop("_id"))
                x["updated_at"] = str(x.pop("updated_at"))
                results[x["id"]] = x

        if model != "" and model != None:
            results = self.filter_perfect_match(results, "brand_model", model)
        if location != "" and location != None:
            results = self.filter_perfect_match(results, "location", location)
        if year != "" and year != None:
            results = self.filter_perfect_match(results, "year", year)
        if brand != "" and brand != None:
            results = self.filter_perfect_match(results, "brand_code", brand)
        if fuel_type != "" and fuel_type != None:
            results = self.filter_perfect_match(results, "fuel_type", fuel_type)

        if page_size and page_number:
            results_original = copy.deepcopy(results)
            results = {}
            idx = 1
            last_result_idx = page_size*page_number + 1
            initial_result_idx = page_size*page_number - page_size + 1
            for identifier, element in results_original.items():
                if idx in range(initial_result_idx, last_result_idx) and len(results) < page_size:
                    results[identifier] = element
                idx = idx + 1
            # for idx in range(0, page_size):


        return results

    def filter_by_range(self, results, range):
        pass

    def filter_perfect_match(self, results, key, string):
        filtered_results = {}
        for identifier, element in results.items():
            if element.get(key) == string:
                filtered_results[identifier] = element
        return filtered_results

    def save_in_mongo(self, payload, collection):
        documents = self.db[collection]
        documents.insert_one(payload).inserted_id

    def get_frequent_searches(self, type='top'):
        model_searches = {}
        model_details = {}
        top_ten = []
        
        my_collection = self.db['search_payloads']
        for search_payload in my_collection.find({}):
            search_payload.pop("_id")
            model = search_payload.get('model')
            if not model_searches.get(model):
                model_searches[model] = 0
            model_searches[model] = model_searches[model] + 1

        sorted_by_value = dict(sorted(model_searches.items(), key=lambda x: x[1], reverse=True))

        for model, searches in sorted_by_value.items():
            if model != "":
                top_ten.append(model)
            if len(top_ten) == 10:
                break

        my_collection = self.db['cars']
        for car in my_collection.find({"brand_model":{"$in":top_ten}}):
            car["id"] = str(car.pop("_id"))
            car["updated_at"] = str(car.pop("updated_at"))
            model = car.get('brand_model')
            price = car.get('price')
            currency = car.get('currency')
            model = car.get('model')
            mileage_raw = car.get('mileage_raw')
            location = car.get('location')
            year = car.get('year')
            fuel_type = car.get('fuel_type')
            if price and model != "":
                if not model_details.get(model):
                    model_details[model] = {
                        'photo_url' : car.get('photo_url'),
                        'model' : model,
                        'min_price' : price,
                        'currency' : currency,
                        'model' : model,
                        'mileage_raw' : mileage_raw,
                        'location' : location,
                        'year' : year,
                        'fuel_type' : fuel_type,
                    }
                elif price < model_details[model]["min_price"]:
                    model_details[model]["min_price"] = price

        return model_details

    def get_recently_added(self, quantity):
        results = []

        my_collection = self.db['cars']
        for car in my_collection.find({}).sort("date",-1).limit(quantity):
            car["id"] = str(car.pop("_id"))
            car["updated_at"] = str(car.pop("updated_at"))
            results.append(car)

        return results

    def get_car_by_ids(self, ids):
        results = []

        object_ids = []
        for identifier in ids:
            object_ids.append(ObjectId(identifier))

        my_collection = self.db['cars']
        for car in my_collection.find({"_id":{"$in":object_ids}}):
            car["id"] = str(car.pop("_id"))
            car["updated_at"] = str(car.pop("updated_at"))
            results.append(car)
        return results


            
