import requests

url = 'https://data-cloud.flightradar24.com/zones/fcgi/feed.js'
params = {'adsb': '1',
          'air': '1',
          'bounds': '48.30061518188964%2C37.567150067916806%2C27.21118459491588%2C42.12920833343368',
          'estimated': '1',
          'faa': '1',
          'flarm': '1',
          'gliders': '1',
          'gnd': '1',
          'limit': '5000',
          'maxage': '14400',
          'mlat': '1',
          'satellite': '1',
          'stats': '1',
          'vehicles': '1'}
url += "?" + "&".join(["{}={}".format(k, v) for k, v in params.items()])
headers = {'accept': 'application/json',
           'accept-encoding': 'gzip, br',
           'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
           'cache-control': 'max-age=0',
           'origin': 'https://www.flightradar24.com',
           'referer': 'https://www.flightradar24.com/',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-site',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

timeout = 30
data = None
cookies = None

response = requests.get(url, params, headers = headers, timeout = timeout, data = data, cookies = cookies)
content = response.json()

#csv_data = 'id, Код ICAO, Широта, Долгота, Направление, Высота (футы), Скорость относительно земли, squawk, 8, Модель самолёта, Регистрация самолёта, time, Код аэропорта вылета, Код аэропорта прилёта, Номер полёта, 15, 16, Позывной, 18, Код авиакомпании\n'
csv_data = ['id', 'Код ICAO', 'Широта', 'Долгота', 'Направление', 'Высота (футы)', 'Скорость относительно земли', 'squawk', '8', 'Модель самолёта', 'Регистрация самолёта', 'time', 'Код аэропорта вылета', 'Код аэропорта прилёта', 'Номер полёта', '15', '16', 'Позывной', '18', 'Код авиакомпании']




while True:
    print("1 - .csv mode \n2 - PostgreSQL mode \nother - stop")
    menu_var = str(input())


    if menu_var == 1:
        for i in content:
            try:
                lat, lon = int(content[i][1]), int(content[i][2])
            except:
                continue
            if len(str(i)) == 8:
                #csv_data += str(i)
                csv_data.append(str(i))
                for j in content[i]:
                    #csv_data += (', ' + str(j))
                    csv_data.append(str(j))
                #csv_data[-1] += '\n'



        counter = 0
        for i in range(0, len(csv_data)):
            counter += 1
            if counter != 1 and (counter == 9 or counter == 16 or counter == 17 or counter == 19):
                csv_data[i] = 'for_delete'
            if counter == 20:
                counter = 0
            if csv_data[i] == '':
                csv_data[i] = 'empty'
            if csv_data[i] == '\n':
                csv_data[i] = 'empty\n'

        def condition(elem): return elem != 'for_delete'
        filtered_csv_data = filter(condition, csv_data)
        filtered_csv_data = list(filtered_csv_data)



        string_csv = ''
        counter = 0
        for i in filtered_csv_data:
            string_csv += i
            if counter == 15:
                string_csv += '\n'
                counter = 0
                continue
            else:
                counter += 1
                string_csv += ', '


        with open('flights.csv', 'w', encoding='utf-8') as f:
            f.write(string_csv)
        break

    if menu_var == 2:
        print("plug") #using table feeder here
        #user = str(input('username:'))
        #password = str(input('password:'))
        #host = str(input('host:'))
        #port = str(input('port:'))
        #table_feeder(username: username, password: password, host: host, port:port)      
        break

    else:
        break


