import openai
from datetime import datetime
import uuid
import os



openai_api_key = os.environ.get('OPENAI_API_KEY')

def generate_openai_prompt(user_input):
    openai.api_key = openai_api_key
    current_datetime = datetime.now()
    unique_id = str(uuid.uuid4())

    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
{
  "role": "user",
  "content": f"Build a Google Calendar event with a meeting link (in dictionary format) with the following details and provide the object only without additional explanation:\
    \n\n{user_input}\n\n The fields I need in this dictionary are: summary, location, description, colorId, start, end,\
    recurrence, and conferenceData. Here are the rules to follow:\n\n\
    1. Origin datetime is {current_datetime}, so if the user asks to set an event in the future but does not specify any \
    date or time, calculate the date and time based on {current_datetime}.\n\
    2. If the user provides the day in this format:mon=Monday, tue=Tuesday, wed=Wednesday, thu=Thursday, fri=Friday, sat=Saturday, sun=Sunday, and doesn't specify a date, set the\
    date to the first upcoming date on that day. If the user's requested day matches {current_datetime.day}, create the event\
    for next week on that day from {current_datetime.date} and not on {current_datetime.day}.\n\
    3. If the user only provides the date and not the time, set the default time to 10am on that date.\n\
    4. If the user provides the time but doesn't provide any date, set the date to {current_datetime.date}.\n\
    5. If there is no indication of a meeting (user doesn't provide information about date or time, doesn't mention meeting\
    the other person, or asks to revisit the idea later), set a reminder with summary: 'Event Reminder', and set all\
    conferenceData and createRequest to empty strings.\n\
    6. Never create events recurrently unless asked for.\n\
    7. Default fields for different keys are as follows:\n\nsummary: Virtual Event\nlocation: Online\ndescription: Virtual\
    meeting to discuss key topics and collaborate online.\ncolorId: 6\nstart timeZone: America/Vancouver\n\
    end timeZone: America/Vancouver\nrecurrence: once, daily\nrequestId for the conference: {unique_id}\n\
    conferenceSolutionKey type: hangoutsMeet.\n8. Enclose the key-value pairs in double quotes.\n\
    9. Keep the event object the same length with the same keys to prevent syntax errors.\n\
    10. Please make sure to follow all these rules.\
    Here are some example prompts with the outputs expected from you:\
        Can we do the 28th at 2pm? create an event for the upcoming 28th at 2pm.\
        I want to talk tue 14:00. create an event for the upcoming Tuesday in the future at 14:00.\
        Let's do the 27th. (no time given). Create an event for the 27th at 10am.\
        No, I can't do fri at 3pm. How about next tuesday at 2pm? create an event for next Tuesdat at 2pm.\
        Does Fri in 2 weeks at 10am work for you? create an event on Friday in two weeks at 10am.\
        Can we revisit this in 2 weeks? (set a reminder to revisit, instead of call). don't create any meeting link or info, just a reminder."
}

]
    response = openai.chat.completions.create(
        model= 'gpt-3.5-turbo',
        messages=messages,
        max_tokens=500
    )

    response_content = response.choices[0].message.content
    
    start_index = response_content.find("{")
    end_index = response_content.find("}\n}")
    event_content = response_content[start_index:end_index+4]
    event = eval(event_content)
    print(response_content)
    return event

# # Get user input
# user_input = input("Enter the details for the calendar event:\n")

# # Generate OpenAI prompt
# generated_prompt = generate_openai_prompt(user_input)
# print(generated_prompt)

# if __name__ == "__main__":
#     main()