from flask_restful import Resource
from flask_restful import reqparse
import pandas as pd


class Locations(Resource):
    def get(self):
        data = pd.read_csv('locations.csv')  # read local CSV
        return {'data': data.to_dict()}, 200  # return data dict and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('locationId', required=True, type=int, location="values")  # add args
        parser.add_argument('name', required=True, location="values")
        parser.add_argument('rating', required=True, type=float, location="values")
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('locations.csv')

        # check if location already exists
        if args['locationId'] in list(data['locationId']):
            # if locationId already exists, return 401 unauthorized
            return {
                'message': f"'{args['locationId']}' already exists."
            }, 409
        else:
            # otherwise, we can add the new location record
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'locationId': [args['locationId']],
                'name': [args['name']],
                'rating': [args['rating']]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('locations.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('locationId', required=True, type=int, location="values")  # add args
        parser.add_argument('name', store_missing=False, location="values")  # name/rating are optional
        parser.add_argument('rating', store_missing=False, type=float, location="values")
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('locations.csv')

        # check that the location exists
        if args['locationId'] in list(data['locationId']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['locationId'] == args['locationId']]

            # if name has been provided, we update name
            if 'name' in args:
                user_data['name'] = args['name']
            # if rating has been provided, we update rating
            if 'rating' in args:
                user_data['rating'] = args['rating']

            # update data
            data[data['locationId'] == args['locationId']] = user_data
            # now save updated data
            data.to_csv('locations.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['locationId']}' location does not exist."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('locationId', required=True, type=int, location="values")  # add locationId arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('locations.csv')

        # check that the locationId exists
        if args['locationId'] in list(data['locationId']):
            # if it exists, we delete it
            data = data[data['locationId'] != args['locationId']]
            # save the data
            data.to_csv('locations.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['locationId']}' location does not exist."
            }
