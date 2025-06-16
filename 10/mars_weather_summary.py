import pymysql


class MySQLHelper:
    def __init__(self, host='localhost', user='root', password='codyssey', database='mars_db'):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4'
        }
    
    def get_connection(self):
        return pymysql.connect(**self.config)
    
    def execute_query(self, query, params):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()


def read_csv_file():
    with open('3-1/mars_weathers_data.CSV', 'r', encoding='utf-8') as file:
        content = file.read()
        return content.strip().split('\n')[1:]


def main():
    db_helper = MySQLHelper()
    weather_data = read_csv_file()
    
    for line in weather_data:
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) < 4:
            continue
        
        mars_date = parts[1]
        temp = int(float(parts[2]))
        storm = int(parts[3])
        
        db_helper.execute_query(
            'INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)',
            (mars_date, temp, storm)
        )


if __name__ == '__main__':
    main()