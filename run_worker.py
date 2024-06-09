import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import FetchNewsWorkflow
from activities import fetch_news

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="news-task-queue",
        workflows=[FetchNewsWorkflow],
        activities=[fetch_news],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
