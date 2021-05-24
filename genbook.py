import requests
import json

s = requests.Session()


# function to get the open time slots for out selected day
def find():
    global date
    date = input('What day would you like the schedule your appointment?' + ' For example:: for September 21, enter 0921.... ')

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }

    # page_one = s.get('https://www.genbook.com/bookings/api/serviceproviders/30259845/services/1236342333?&size=100&page=1', headers=headers)
    
    # Page for time slots
    page_two = s.get('https://www.genbook.com/bookings/api/serviceproviders/30259845/services/1236342333/resources/1236539394?&day=2021' + date +'L&view=day', headers = headers)
    data = page_two.json()
    print("These are the available times for the date given ::: ")

    if 'times' not in data:
        print('No times available! Try another day::: ')
        print()
        find()
    else:
        # LIST OF TIMES FOR CHOSEN DATE
        for time in data["times"]:
            slot = time[9:13]
            print(slot)
            
            
find()


# function for booking time slot
def go():
    choice = input('Input the time you would like ::: ')

    book = {
        'lmb': 'false',
        'resourceid': '1236539394',
        'serviceid': '1236342333',
        'sourceid': '1029',
        'starttime': '2021' + date + 'T' + choice + '00L'
    }

    head = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }

    page_three = s.post('https://www.genbook.com/bookings/api/serviceproviders/30259845/bookings', data=json.dumps(book), headers=head)

    data = page_three.json()

    num = str(data['id'])

    info = {
        'address':  {'id': '', 'address1': '', 'address2': '', 'city': '', 'postalcode': '', 'state': '', 'countrycode': ''},
        'countrycode': 'US',
        'email': 'xxx@gmail.com',
        'firstname': 'John',
        'lastname': 'Doe',
        'phone': '1234567891',
        'specialrequests': ''
    }

    confirm = s.put('https://www.genbook.com/bookings/api/serviceproviders/30259845/bookings/' + num, data=json.dumps(info), headers=head)
    dup = s.put('https://www.genbook.com/bookings/api/serviceproviders/30259845/bookings/' + num, data=json.dumps({'status': '2'}), headers=head)

    soup = dup.json()

    conf = soup['confirmation']
    price = soup['service']['price']

    print()
    print('SUCCESS')
    print()
    print(conf)
    print(price)
    
    
go()
