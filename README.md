# AskGpt Bot README

The AskGpt Bot is a Python script designed to interact with the Mattermost messaging platform and utilize OpenAI's GPT-3.5 engine to provide responses to user input. The bot reads user messages, processes them using the OpenAI API, and returns relevant responses. Additionally, the bot stores user interactions in a SQLite database for logging and analysis.

## Setup and Configuration

1. Python Environment:
   - Ensure you have Python installed on your system. The bot is compatible with Python 3.x.

2. Install Dependencies:
   - The bot requires several external libraries. To install them, run the following command in your terminal:
   - The file being dockerised, user has to run: "docker-compose build" on terminal
   - After your image is built run "docker-compose up" on terminal
   - After your image is up and running, log onto Mattermost

3. API Keys and Credentials:
   - Input the necessary API keys and credentials:
     - OpenAI API Key: Register on the OpenAI website to get an API key for GPT-3.5
     - Mattermost Bot Credentials: Create a bot user in your Mattermost instance and obtain the bot's username and token.
     - Mattermost Server URL: Provide the URL of your Mattermost server.
     - Profile Creation URL: Provide the URL of your Fasthost server.

4. Environment Variables:
   - Create a file named `credentials.env` in the same directory as the bot script.
   - Add the following content to the `credentials.env` file, replacing the placeholders with your actual credentials:

   ```
   URL=Your_Mattermost_Server_URL
   BOT_USERNAME=Your_Mattermost_Bot_Username
   BOT_PASSWORD=Your_Mattermost_Bot_Password
   SERVER_URL=Your_Mattermost_Server_URL
   SCHEME=https  # Change to 'http' if your server uses HTTP instead of HTTPS
   OPENAI_API_KEY=Your_OpenAI_API_Key
   ```

## Database Setup

The bot uses an SQLite database to store user interaction logs. The `your_database` database will be created automatically when the bot is executed.


## Functionality

1. Response Generation:
   - The bot listens for user messages and responds to specific commands:
     - Typing 'hi' will trigger a welcome message.
     - Typing 'AskGptPayload' will display the payload used to call the OpenAI API.
     - Typing 'AskGpt:' followed by a user input will invoke the GPT-3 engine to generate a response.
     - Typing 'ShowResponse:' will display the last response sent by the bot to the user.
     - Typing 'Help' or 'Manual' will show this file.

2. Keyword Profile Generation:
   - Typing 'profile_name=' followed by a name and keywords separated by commas will create a keyword profile.

3.  Data Retrieval and Display:
   - Typing 'Today_Summary: @user_name ' will display a summary of the inputted user interactions grouped by username of that date.
   - Typing 'All_Summary' will display a summary of last 30 user interactions grouped by username and date.
   - Typing 'Self_Summary' will display a summary of his/her last 30 interactions grouped by username and date.

## Important Notes

- The bot requires a connection to the Mattermost server to function correctly.
- Ensure the Mattermost Bot user has the necessary permissions to post messages in the intended channels.
- The `openai.api_key` variable should be set with a valid GPT-3.5 API key.
- The database `user_data_16.db` will be created in the same directory as the script.
- The database schema includes a `users` table to store user interactions.

Please ensure that you comply with any terms of service and privacy policies of the services used (e.g., OpenAI and Mattermost) while deploying and using this bot.

**Note:** This README provides an overview of the bot's functionality. For detailed implementation and usage, please refer to the code comments and the OpenAI and Mattermost documentation.

## Troubleshooting

If you encounter any issues or errors, please check the following:

- Verify that the environment variables in `credentials.env` are correctly set.
- Ensure you have the required permissions to access the Mattermost server and create the bot.
- Check the Mattermost server logs for any error messages related to the bot.
- Review the bot script's code and comments for possible debugging clues.
- Ensure you have the correct versions of the required Python libraries installed.

If problems persist, refer to the specific documentation for the platforms and libraries used in the bot.

Happy Chatting with AskGpt Bot! 🤖
