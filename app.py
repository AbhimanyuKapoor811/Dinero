import openai
import requests
import os
from dotenv import load_dotenv
import json
from mattermostdriver import Driver
import sqlite3
from datetime import datetime
from time import sleep

load_dotenv('credentials.env')
last_response_to_user = {}
user_logs = []

url = os.getenv('URL')
bot_username = os.getenv('BOT_USERNAME')
bot_password = os.getenv('BOT_PASSWORD')
server_url = os.getenv('SERVER_URL')
scheme = os.getenv('SCHEME')
openai.api_key = os.getenv('OPENAI_API_KEY')


def read_command_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as command_file:
            return command_file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


# Replace 'path/to/readme.md' with the actual path to your readme.md file.
command_contents = read_command_file('/home/akapoor/Final_Project/Commands.md')


# Function to create the table
def create_table():
    # Connect to the database (if it doesn't exist, it will be created)
    conn = sqlite3.connect("user_data_17.db")

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Define the SQL command to create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users  (
        user_id TEXT,
        username TEXT NOT NULL,
        userinput TEXT NOT NULL,
        useroutput TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """

    # Execute the SQL command to create the table
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function to insert data into the table
def insert_data(user_id, username, userinput, useroutput):
    # Connect to the database
    conn = sqlite3.connect("user_data_17.db")
    cursor = conn.cursor()

    # Get the current real-time timestamp
    timestamp = str(datetime.now())
    # Execute the SQL command with the provided values
    cursor.execute("""INSERT INTO users (user_id, username, userinput,
                    useroutput, timestamp) VALUES (? , ?, ?, ?, ?) """,
                   (user_id, username, userinput, useroutput, timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function to fetch all data from the table
def fetch_all_data():
    # Connect to the database
    conn = sqlite3.connect("user_data_17.db")
    cursor = conn.cursor()

    # Define the SQL command to fetch all data from the table
    select_query = "SELECT * FROM users;"

    # Execute the SQL command and fetch all data
    cursor.execute(select_query)
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    result_list = []
    # Loop through each row and create a dictionary for each row
    for row in data:
        user_id, username, userinput, useroutput, timestamp = row
        result_dict = {
            "user_id": user_id,
            "username": username,
            "userinput": userinput,
            "useroutput": useroutput,
            "timestamp": timestamp
        }
        result_list.append(result_dict)

    # Update the user_logs list with the fetched data
    global user_logs
    user_logs = result_list

    return result_list


def list_to_string(input_list, separator=""):
    return separator.join(input_list)


def fetch_userdata_by_username(database, username):
    # Connect to the database
    username = username.strip()
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Define the SQL command to fetch data
    # for the provided username from the table
    cursor.execute("""SELECT user_id, userinput, useroutput,
                   timestamp FROM users WHERE username = ? ;""", [username])
    # Fetch all data for the provided usernames
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    result_list = []
    # Loop through each row and create a dictionary for each row
    for row in data:
        user_id, userinput, useroutput, timestamp = row
        result_dict = {
            "user_id": user_id,
            "username": username,
            "userinput": userinput,
            "useroutput": useroutput,
            "timestamp": timestamp
        }
        result_list.append(result_dict)
    return result_list


def get_latest_data():
    # Connect to the SQLite database
    conn = sqlite3.connect("user_data_17.db")
    cursor = conn.cursor()
    # Create the SQL query to retrieve the latest data
    sql_query = "SELECT useroutput FROM users ORDER BY timestamp DESC LIMIT 1;"
    # Execute the query and fetch the latest data
    cursor.execute(sql_query)
    latest_data = cursor.fetchone()
    # Close the connection
    conn.close()

    return latest_data


def group_responses_by_username_and_date(database_file):
    conn = sqlite3.connect(database_file)
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Define the SQL command to group the responses by username and date (based on timestamp)
        group_query = """
            SELECT username, date(timestamp) AS response_date, COUNT(*) AS num_responses
            FROM users
            GROUP BY username, date(timestamp)
            ORDER BY username, date(timestamp);
        """

        # Execute the SQL command
        cursor.execute(group_query)

        # Fetch all grouped data
        grouped_data = cursor.fetchall()

        # Close the connection
        conn.close()

        return grouped_data

    except sqlite3.Error as e:
        print(e)


def markdownTable(data):
    # Extracting the headers from the first dictionary
    headers = data[0].keys()

    # Generate the Markdown table string
    md_table_string = "| " + " | ".join(headers) + " |\n" + "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for row in data:
        md_table_string += "| " + " | ".join(str(value) for value in row.values()) + " |\n"

    # Print or use the md_table_string as needed
    return md_table_string


def list_of_tuples_to_md_string(data):
    # Extracting the headers from the first tuple
    headers = ["UserName", "Date", "NumberofIntents"]

    # Generate the Markdown table string
    md_table_string = "| " + " | ".join(headers) + " |\n" + "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for row in data:
        md_table_string += "| " + " | ".join(str(value) for value in row) + " |\n"

    return md_table_string


def extract_keywords(final_output):
    keywords = final_output.split(',')
    keywords_list = []

    for i, keyword in enumerate(keywords, start=1):
        keyword_dict = {
            "keyword": keyword.strip(),
            "lock": i == 1,
            "sort_order": i - 1
        }
        keywords_list.append(keyword_dict)

    return keywords_list


def main():
    # Initialises the credentials of the user on which the messages and
    # responses are to be shown
    driver = Driver({'url': server_url,
                     'login_id': bot_username,
                     'token': bot_password,
                     'scheme': scheme,
                     'port': 443})
    driver.login()

    async def response_handler(message):
        # Filters the required response from the json file into a string format
        message_json = json.loads(message)
        if 'data' in message_json.keys():
            data_message_json = message_json['data']
            if 'post' in data_message_json:
                user_name_message_json = data_message_json["channel_display_name"]
                post_data_message_json = data_message_json['post']
                output_json = json.loads(post_data_message_json)
                user_id = output_json['user_id']
                result = output_json['message']
                channel_id = output_json['channel_id']
                bot_responses(result, user_id, channel_id,
                              user_name_message_json)

    def ask_gpt_response(user_message):
        '''Calls the openai API passes the sliced user input
        and returns the response'''
        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=user_message,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.7
        )
        # Filters the required message from the dictionary provided by ChatGPT
        chatbot_response = response.choices[0].text.strip()

        return f"{chatbot_response}"

    def bot_responses(result, user_id, channel_id, user_name_message_json):
        '''Checks the user inputs and prints
        the appropriate response on the production server'''
        # ... Existing code ...
        if result.lower().startswith('hi'):
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': ('Welcome to AskGpt.'
                            ' Please write your intent after typing '
                            '\"AskGpt:\" ')
                                    })
        if result.startswith('AskGptPayload'):
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': """```
engine='text-davinci-003',
prompt=user_message,
max_tokens=3000,
n=1,
stop=None,
temperature=0.7
```
"""
                                    })
        final_output = ask_gpt_response(result[6:] + """separate
                                        them with commas and not in a numbered list format""")

        if result.startswith('AskGpt: '):
            insert_data(user_id, user_name_message_json, result[7:],
                        final_output)
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': final_output
                                    })
            sleep(3)
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': """If you want to make a Keyword Profile,
                start your message with profile_name= and type in the name
                  with which you want to crete the profile"""
                                    })
            if user_id in last_response_to_user:
                last_response_to_user[user_id] = (final_output)
            else:
                last_response_to_user[user_id] = (final_output)

        if result.startswith('ShowResponse:'):
            if user_id in last_response_to_user.keys():
                driver.posts.create_post({
                    'channel_id': channel_id,
                    'message': last_response_to_user[user_id]
                                        })
        if result == "Help" or result == "Manual":
            if command_contents:
                driver.posts.create_post({
                    'channel_id': channel_id,
                    'message': command_contents
                                        })
        profile_name = result[13:]
        if result.startswith('profile_name='):
            gpt_latest_data = get_latest_data()
            result_string = ', '.join(str(item) for item in gpt_latest_data)
            keywords = extract_keywords(result_string)
            payload = json.dumps({
                    "profile_name": profile_name,
                    "rotate": False,
                    "keywords_list": keywords
                    }, indent=2, ensure_ascii=False)
            headers = {
                        'Content-Type': 'application/json',
                        'Authorization': 'ApiKey Gauravvv:4fd1bcbd026d047c3465afd130159a1e70a4088c'
                      }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 201:
                driver.posts.create_post({
                    'channel_id': channel_id,
                    'message': "Your profile is created."
                                        })
            else:
                driver.posts.create_post({
                    'channel_id': channel_id,
                    'message': "Try again"
                                    })

        if result.startswith('Today_Summary'):
            grouped_data = group_responses_by_username_and_date("user_data_17.db")
            grouped_table = list_of_tuples_to_md_string(grouped_data)
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': grouped_table
            })

        if result.startswith('ShowTable'):
            return_list = fetch_all_data()
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': markdownTable(return_list)
                                    })
        username = result[10:]
        if result.startswith('ShowStats:'):
            return_list = fetch_userdata_by_username("""user_data_17.db""",
                                                     username)
            driver.posts.create_post({
                'channel_id': channel_id,
                'message': markdownTable(return_list)
                                    })
    driver.init_websocket(response_handler)


if __name__ == '__main__':
    # Create the table (if not already created)
    create_table()
    main()
