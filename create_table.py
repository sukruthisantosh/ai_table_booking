import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:9000")
def create_reservations_table(dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb')
    table = dynamodb.create_table(
        TableName='Reservations',
        KeySchema=[
            {
                'AttributeName': 'full_name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'booking_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'booking_id',
                # AttributeType refers to the data type 'N' for number type and 'S' stands for string type.
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'full_name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
            # WriteCapacityUnits set to 10 writes per second
        }
    )
    return table


if __name__ == '__main__':
    booking_table = create_reservations_table()
    print("Status:", booking_table.table_status)
