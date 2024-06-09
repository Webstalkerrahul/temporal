from temporalio import workflow
from activities import fetch_news
from datetime import timedelta

@workflow.defn
class FetchNewsWorkflow:
    @workflow.run
    async def run(self, name: str) -> dict:
        result = await workflow.execute_activity(
            fetch_news,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return result
    

