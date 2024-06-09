import asyncio
from temporalio.client import Client

from workflows import FetchNewsWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    news = await client.execute_workflow(
        FetchNewsWorkflow.run,
        "News",
        id="temporal-community-workflow",
        task_queue="news-task-queue",
    )
    
    articles = news.get('articles', [])
    for article in articles:
        title = article.get('title')
        publishedAt = article.get('publishedAt')
        description = article.get('description')
        content = article.get('content')
        print(f"Title: {title}")
        print(f"Published At: {publishedAt}")
        print(f"Description: {description}")
        print(f"Content: {content}")
        print("-" * 40)
    return articles

if __name__ == "__main__":
    asyncio.run(main())
