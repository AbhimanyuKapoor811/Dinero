# Response Generation:
   - The bot listens for user messages and responds to specific commands:
     - Typing 'hi' will trigger a welcome message.
     - Typing 'AskGptPayload' will display the payload used to call the OpenAI API.
     - Typing 'AskGpt:' followed by a user input will invoke the GPT-3 engine to generate a response.
     - Typing 'ShowResponse:' will display the last response sent by the bot to the user.
     - Typing 'Help' or 'Manual' will show this file.

# Keyword Profile Generation:
   - Typing 'profile_name=' followed by a name and keywords separated by commas will create a keyword profile.

# Data Retrieval and Display:
   - Typing 'Today_Summary: @user_name ' will display a summary of the inputted user interactions grouped by username of that date.
   - Typing 'All_Summary' will display a summary of last 30 user interactions grouped by username and date.
   - Typing 'Self_Summary' will display a summary of his/her last 30 interactions grouped by username and date.

