import json
from decimal import Decimal
import boto3

def load_booking(booking_list, dynamodb=None):

    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb')

    booking_table = dynamodb.Table('Reservations')

    for booking in booking_list:
        booking_id = booking['booking_id']
        name = booking['full_name']

        print("Displaying booking data:", booking_id, name)

        booking_table.put_item(Item=booking)


with open("booking_summary.json") as json_file:
    booking_list = json.load(json_file, parse_float=Decimal)

load_booking(booking_list)
