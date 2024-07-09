import asyncio
import os
import aiohttp
import aiofiles


async def process_attachments(data):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in data:
            attachment_url = item.get('AttachmentPath')
            if attachment_url:
                # Extract the filename from the URL
                filename = os.path.basename(attachment_url)
                
                # Specify the path where the file will be saved
                download_path = os.path.join('/data/source', filename)  # Replace with your desired download path
                
                # Add a task to download the PDF asynchronously
                tasks.append(download_pdf(session, attachment_url, download_path))
        
        # Wait for all download tasks to complete
        await asyncio.gather(*tasks)

async def download_pdf(session, url, download_path):
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Save the PDF file
            async with aiofiles.open(download_path, 'wb') as f:
                await f.write(await response.read())
                print(f"Downloaded {os.path.basename(download_path)} successfully.")
    except aiohttp.ClientError as e:
        print(f"Error downloading {url}: {e}")