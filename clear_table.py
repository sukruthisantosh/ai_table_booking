import boto3

def clear_dynamodb_table(table):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    scan = table.scan()

    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'booking_id': each['booking_id'],
                    'full_name': each['full_name']
                }
            )

    print(f"All items deleted from table: {table_name}")


if __name__ == '__main__':
    table_name = 'Reservations'
    clear_dynamodb_table(table_name)
