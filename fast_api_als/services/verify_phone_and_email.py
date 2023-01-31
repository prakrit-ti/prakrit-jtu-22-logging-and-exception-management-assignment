import time
import httpx
import asyncio
import logging
from fast_api_als.constants import (
    ALS_DATA_TOOL_EMAIL_VERIFY_METHOD,
    ALS_DATA_TOOL_PHONE_VERIFY_METHOD,
    ALS_DATA_TOOL_SERVICE_URL,
    ALS_DATA_TOOL_REQUEST_KEY)

"""
How can you write log to understand what's happening in the code?
You also trying to undderstand the execution time factor.
"""
logging.basicConfig(level=logging.DEBUG)
async def call_validation_service(url: str, topic: str, value: str, data: dict) -> None:  # 2
    logging.info('Call Validation Service Initiated')
    st = int(time.time()) * 1000
    if value == '':
        return
    async with httpx.AsyncClient() as client:  # 3
        response = await client.get(url)

    r = response.json()
    data[topic] = r
    en = int(time.time()) * 1000
    logging.info("Call Validation service completed in %d seconds" %(en-st))
    

async def verify_phone_and_email(email: str, phone_number: str) -> bool:
    logging.info("Initiating email and phone verification")
    email_validation_url = '{}?Method={}&RequestKey={}&EmailAddress={}&OutputFormat=json'.format(
        ALS_DATA_TOOL_SERVICE_URL,
        ALS_DATA_TOOL_EMAIL_VERIFY_METHOD,
        ALS_DATA_TOOL_REQUEST_KEY,
        email)
    phone_validation_url = '{}?Method={}&RequestKey={}&PhoneNumber={}&OutputFormat=json'.format(
        ALS_DATA_TOOL_SERVICE_URL,
        ALS_DATA_TOOL_PHONE_VERIFY_METHOD,
        ALS_DATA_TOOL_REQUEST_KEY,
        phone_number)
    email_valid = False
    phone_valid = False
    data = {}

    await asyncio.gather(
        call_validation_service(email_validation_url, "email", email, data),
        call_validation_service(phone_validation_url, "phone", phone_number, data),
    )
    st = int(time.time()) * 1000
    if "email" in data:
        if data["email"]["DtResponse"]["Result"][0]["StatusCode"] in ("0", "1"):
            email_valid = True
    en1 = int(time.time()) * 1000
    if "phone" in data:
        if data["phone"]["DtResponse"]["Result"][0]["IsValid"] == "True":
            phone_valid = True
    en2 = int(time.time()) * 1000
    if email_valid:
        logging.info("Email verified in %d seconds" %(en1 - st))
    else: 
        logging.WARNING("Email not valid")

    if phone_valid:
        logging.info("Phone verified in %d seconds" %(en2 - en1))
    else: 
        logging.WARNING("Phone not valid")
    return email_valid | phone_valid
