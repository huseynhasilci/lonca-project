"""Main file to execute everything."""
import asyncio
import schedule
import time
import os

from utils.helpers.FileReader import FileReader
from utils.DocumentOrganizer import DocumentOrganizer
from utils.MongoDbManager import MongoDBAsync

MONGO_DB_URI = os.environ['MONGO_URL']
MONGO_DB_NAME = 'Products'
MONGO_DB_COLLECTION_NAME = 'Product'

async def job():
    file_reader_obj = FileReader(file_path='lonca-sample.xml')
    xml_root = file_reader_obj.read_xml_file()
    document_organizer = DocumentOrganizer(root=xml_root)
    mongo = MongoDBAsync(MONGO_DB_URI, MONGO_DB_NAME, MONGO_DB_COLLECTION_NAME)

    organized_document_list = document_organizer.orginze_document()

    await mongo.connect()
    await mongo.insert_many(organized_document_list)
    await mongo.close()

async def async_job_wrapper():
    await job()

async def run_scheduled_jobs():
    while True:

        schedule.run_pending()

        await asyncio.sleep(1)

def schedule_job():
    schedule.every(10).seconds.do(lambda: asyncio.create_task(async_job_wrapper()))


async def main():

    schedule_job()

    await run_scheduled_jobs()

if __name__ == '__main__':
    asyncio.run(main())
