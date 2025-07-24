from data_manager import increase_counter, read_counter, get_data
from messenger import send_message

def send_next_message(contact_name):

    counter = read_counter()
    today_data = get_data(counter)

    if today_data is None:
        print("data file has no entry for today's counter")
        raise Exception
    send_message(
        contact_name=contact_name,
        message=today_data,
    )
    increase_counter()