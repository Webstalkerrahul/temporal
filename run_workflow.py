import asyncio
import asyncpg
from datetime import datetime
from temporalio.client import Client
from workflows import FetchNewsWorkflow
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

async def insert_articles(articles):
    conn = await asyncpg.connect(
        user='postgres', 
        password='admin', 
        database='temporal', 
        host='localhost'
    )

    insert_query = """
    INSERT INTO news_articles (title, published_at, description, content)
    VALUES ($1, $2, $3, $4)
    """

    for article in articles:
        title = article.get('title')
        published_at = article.get('publishedAt')
        published_at = datetime.fromisoformat(published_at)
        description = article.get('description')
        content = article.get('content')

        await conn.execute(insert_query, title, published_at, description, content)

    await conn.close()
    print("Articles inserted successfully!")

async def fetch_articles():
    conn = await asyncpg.connect(
        user='postgres', 
        password='admin', 
        database='temporal', 
        host='localhost'
    )
    select_query = """
    SELECT title, published_at, description, content
    FROM news_articles
    """
    rows = await conn.fetch(select_query)
    print("\nFetching articles from the database:")
    for row in rows:
        print("Title:", row['title'])
        print("Published At:", row['published_at'])
        print("Description:", row['description'])
        print("Content:", row['content'])
        print("------------------")

    await conn.close()
    print("-------- END ---------")

async def delete_all_articles():
    conn = await asyncpg.connect(
        user='postgres', 
        password='admin', 
        database='temporal', 
        host='localhost'
    )
    delete_query = """
    DELETE FROM news_articles
    """
    await conn.execute(delete_query)
    await conn.close()
    print("All articles deleted successfully!")

async def update_article():
    conn = await asyncpg.connect(
        user='postgres', 
        password='admin', 
        database='temporal', 
        host='localhost'
    )
    update_query = """
    UPDATE news_articles
    SET content = $1
    WHERE id = $2
    """
    title_to_update = 214
    new_content = "Updated Content"
    await conn.execute(update_query, new_content, title_to_update)
    await conn.close()
    print("Article updated successfully!")

async def send_email(subject, content):
    api_key = 'api_key'
    from_email = 'reachcedricbrown@gmail.com'
    to_email = 'rkakade2143@gmail.com'
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

async def main():
    client = await Client.connect("localhost:7233")

    news = await client.execute_workflow(
        FetchNewsWorkflow.run,
        "News",
        id="news-task-workflow",
        task_queue="news-task-queue",
    )
    
    articles = news.get('articles', [])
    # await insert_articles(articles[0:10])
    # await delete_all_articles()
    # await update_article()
    fetched_articles = await fetch_articles()
    
    # if fetched_articles:
    #     email_content = "<h1>Latest News Articles</h1>"
    #     for article in fetched_articles:
    #         email_content += f"""
    #         <h2>{article['title']}</h2>
    #         <p>Published At:{article['published_at']}</p>
    #         <p>Description: {article['description']}</p>
    #         <p>{article['content']}</p>
    #         <hr>
    #         """
        # await send_email("Latest News Articles", email_content)
    # else:
    #     print("No articles found.")

if __name__ == "__main__":
    asyncio.run(main())
