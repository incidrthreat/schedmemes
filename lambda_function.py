import aiohttp, discord, io, json, random, os
from datetime import datetime

def lambda_handler(event, context):
    # Read the images.json file
    with open('images.json', 'r') as f:
        data = json.load(f)
    
    # Get the current day of the week
    current_day = datetime.today().strftime('%A')
    
    week = datetime.today().isocalendar()[1]
    
    # (odd week !=) or (even week ==)
    if week % 2 == 0 and current_day == "Tuesday":
        image_url = 'https://raw.githubusercontent.com/incidrthreat/schedmemes/main/images/reginald.jpg'
    else:
        # Select a random image from the list for the current day
        image_url = random.choice(data[current_day])
    
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
                    await channel.send(file=discord.File(file, "sched_meme.jpg"))
        await client.close()

    client.run(f"{os.getenv('BOT_TOKEN')}")

    return