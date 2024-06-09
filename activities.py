import aiohttp
from temporalio import activity

@activity.defn
async def fetch_news():
    url = ('https://newsapi.org/v2/everything?'
           'q=tech&'
           'from=2024-06-08&'
           'sortBy=popularity&'
           'apiKey=a9796deae1344ea9883089997c880906')

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {"error": "no data"}
