import aiohttp, discord, io, json, random, os
from datetime import datetime

def lambda_handler(event, context):
    # Read the images.json file
    with open('images.json', 'r') as f:
        data = json.load(f)
    
    # Get the current day of the week
    current_day = datetime.today().strftime('%A')

    # Get the current day of the week
    day = datetime.today()
    
    # Odd or Even week
    week = datetime.today().isocalendar()[1]
    
    # (odd week !=) or (even week ==)
    if week % 2 == 0 and current_day == "Tuesday":
        image_url = 'https://raw.githubusercontent.com/incidrthreat/schedmemes/main/images/reginald.jpg'
    # end of April meme
    elif day.month == 4 and day.day == 30:
        image_url = 'https://raw.githubusercontent.com/incidrthreat/schedmemes/main/images/gonna_be_may.jpg'
    # may the 4th be with you meme
    elif day.month == 5 and day.day == 4:
        image_url = 'https://raw.githubusercontent.com/incidrthreat/schedmemes/main/images/may_the_fourth.jpg'
    else:
        # Select a random image from the list for the current day
        image_url = random.choice(data[current_day])

    ext = str.split(image_url, ".")[-1]
    
    # Post the image to Discord
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        channel = client.get_channel(int(os.getenv('CHANNEL_ID')))
        # image_data = requests.get(image_url).content
        async with aiohttp.ClientSession() as session: # creates session
            async with session.get(image_url) as resp: # gets image from url
                img = await resp.read() # reads image from response
                with io.BytesIO(img) as file: # converts to file-like object
                    await channel.send(file=discord.File(file, f"sched_meme.{ext}"))
        await client.close()

    client.run(f"{os.getenv('BOT_TOKEN')}")

    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully posted: {image_url}")
    }