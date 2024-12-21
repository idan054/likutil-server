from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from api.config import Config, DeliveryMethod
from api.services.baldar_service import transform_woo_to_baldar, create_baldar_task, create_baldar_kamatra_task
from api.services.lionwheel_service import transform_woo_to_lionwheel, create_lionwheel_task
from api.services.models import WooAuthData, EmailRequest, CreateDeliveryRequest
from api.services.send_email import send_email
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import logging
from openai import OpenAI
import os


app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root Endpoint
@app.get("/", summary="API Version Checker",
         description="Root endpoint with version status"
         )
def home():
    ver = 36
    return {"status": "ok", f"version {ver}": ver}


# Endpoint to handle WooCommerce callback
@app.post("/woo-auth-callback", summary="WooCommerce Auth Callback Handler")
async def handle_auth(data: WooAuthData):
    # Log the received data
    print("XXXX")
    print("Received WooCommerce Auth Data:", data)

    # Example response
    return {"status": "success", "message": "Auth data received successfully"}


@app.post("/api/send-email", summary="Send Email", description="Send an email to a specified recipient")
def send_email_endpoint(email_request: EmailRequest):
    return send_email(email_request.subject, email_request.body, email_request.to_email)


@app.post("/api/create-delivery", summary="Create Delivery Task",
          description="Create a delivery task for the specified company")
def create_task(
        woo_order: Optional[CreateDeliveryRequest] = None,
        method: str = Query(..., description="", enum=list(DeliveryMethod.__members__.keys())),
        key: Optional[str] = Query(None, description="Token or Client ID"),
        isConnectionTest: bool = Query(False, description="Use predefined test data (true/false)")
):
    try:
        # If isConnectionTest is True, use test data
        if isConnectionTest:
            woo_order_data = Config.TEST_WOO_ORDER
        else:
            if woo_order is None:
                raise HTTPException(status_code=400, detail="woo_order data is required")
            woo_order_data = woo_order.dict()

            # HANDLING ANY NON CUSTOM NON-BALDAR METHOD
        if method == "lionWheel":
            lionwheel_data = transform_woo_to_lionwheel(woo_order_data)
            response = create_lionwheel_task(lionwheel_data, key)
            return response


            # THAN HANDLING BALDAR METHODS
        elif method in DeliveryMethod.__members__:
            baldar_data = transform_woo_to_baldar(woo_order_data, key)
            api_url = DeliveryMethod[method].value  # Access Needed host Based eNum Key & Value
            response = create_baldar_task(baldar_data, api_url)
            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")



# Set up logging
logging.basicConfig(level=logging.INFO, format='BITON %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

@app.get("/getGptResp")
async def handle_get_gpt_response(request: Request):
    query_params = dict(request.query_params)
    answer = get_gpt_response('מה צבע העיניים של ביבי?')
    logger.info(f"GET request received with query params: {query_params}")
    return JSONResponse(content={"status": "GET received", "data": answer})

def get_gpt_response(user_message):
    print('api_key')
    print(api_key)
    print('client KEY')
    print(client.api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "text": "---\n\n### You are a supportive and empowering assistant designed to help students with ADHD. Your role is to provide clear, concise, and motivating guidance for managing busy schedules, handling multiple tasks without becoming overwhelmed, and ensuring progress toward goals. Focus on what matters most at each moment and keep communication simple and actionable.\n\nYour tasks include:\n\n1\\. **Morning routines and daily plans:**\n\n\\- Greet the user based on the time of day (e.g., \"Good morning!\").\n\n\\- Clearly outline 3-5 key goals for the day, including study tasks, social activities, meals, and self-care.\n\n\\- Highlight what the user should focus on right now (e.g., morning routine).\n\n2\\. **Task-by-task focus:**\n\n\\- Only mention tasks relevant to the current time or immediate priority.\n\n\\- Avoid overwhelming the user with too many details at once.\n\n3\\. **Encouragement and progress tracking:**\n\n\\- Use positive and motivating language to keep the user engaged.\n\n\\- Celebrate successes, even small ones, and adjust plans if needed.\n\n4\\. **Dynamic flexibility:**\n\n\\- If plans need to change, provide an updated, clear focus for the current moment.\n\n5\\. **Prioritization and task decomposition:**\n\n\\- Help the user break down monthly and weekly tasks into manageable daily goals.\n\n\\- Ensure prioritization of tasks so that deadlines are met and everything gets completed on time.\n\n\\- Continuously remind the user of their progress toward their broader objectives and how each task contributes to their general goals.\n\n6\\. **Managing overwhelm:**\n\n\\- Recognize when the user feels overwhelmed and provide simple, calming strategies.\n\n\\- Break tasks into the smallest possible steps and suggest focusing on one step at a time.\n\n\\- Offer supportive reminders to take breaks, breathe, and stay grounded.\n\n7\\. **Gamified progress tracking:**\n\n\\- Assign points to tasks based on their difficulty and importance (e.g., easy tasks = 5 points, challenging tasks = 15 points).\n\n\\- Help the user aim for a daily goal of 50 points to stay motivated.\n\n\\- Provide encouraging feedback as points are earned throughout the day.\n\n8\\. **End-of-day review:**\n\n\\- At the end of each day, review the tasks completed and any tasks that remain.\n\n\\- Provide positive reinforcement for what was achieved.\n\n\\- Suggest adjustments for the next day to ensure priorities are met and the workload feels manageable.\n\n9\\. **Keep it concise:**\n\n\\- Responses should be short (1-3 sentences) and action-oriented.\n\n**Key tone:** Friendly, empowering, and focused on helping the user feel confident, in control, and free from overwhelm.\n\n### Special Feature: Managing Overwhelm and Positive Reinforcement\n\n1\\. Recognize when the user is feeling overwhelmed and provide calming, supportive messages.\n\n2\\. Suggest focusing on one small step at a time to create a sense of progress and control.\n\n3\\. Always provide encouragement for effort, even if tasks were not completed.\n\n4\\. Remind the user of what truly matters, without judgment, and offer a new prioritization plan.\n\n5\\. Suggest actionable alternatives to complete the most important tasks:\n\n\\- Shift unfinished tasks to the next day.\n\n\\- Focus on critical priorities for upcoming deadlines.\n\n### Examples of Communication:\n\n#### Encouraging message after a busy day:\n\n\"Hey [Name], today was a busy day, and it's totally okay that not everything got done. The most important thing now is finishing Chapter 4. Let’s start with 30 minutes on it tomorrow morning. You're doing great, and I’m proud of you! 💛\"\n\n#### Offering new priorities:\n\n\"It looks like we didn’t finish the presentation today, but that’s okay. It’s a priority for Wednesday’s deadline, so we’ll focus on it tomorrow. We can spread out the other tasks over the rest of the week. Let’s keep going together! 😊\"\n\n#### Gentle redirection:\n\n\"[Name], I know today didn’t go as planned, and that’s completely fine. How about we leave the smaller task for tomorrow and focus on what’s most important: finishing Chapter 4. This will make the biggest difference! You’ve got this! 💪\"\n\n#### End-of-day review example:\n\n\"Hi [Name], great effort today! 🎉 You completed 3 out of 5 tasks, which is awesome progress. For tomorrow, let’s prioritize finishing the draft and preparing for the presentation. You’re doing a fantastic job, and I’m here to keep you on track! 🌟\"\n\n",
                        "type": "text"
                    }
                ]
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.66,
        max_completion_tokens=188,
        top_p=1,
        frequency_penalty=1.4,
        presence_penalty=0.98
    )
    print('XXXXX')
    print(response.choices[0].message.content)
    return response.choices[0].message.content

@app.get("/liorWaBot")
async def handle_get(request: Request):
    query_params = dict(request.query_params)
    logger.info(f"GET request received with query params: {query_params}")
    return JSONResponse(content={"status": "GET received", "data": query_params})



logger = logging.getLogger("uvicorn.error")


@app.post("/liorWaBot")
async def handle_post(request: Request):
    try:
        body = await request.json()
        logger.info(f"POST request received with body: {body}")

        # Check conditions
        if (
                body.get("typeWebhook") == "incomingMessageReceived" and
                body.get("senderData", {}).get("chatId") == "120363360946946323@g.us"
        ):
            try:
                print('SOPHY GROUP MESSAGE FOUND')
                # Extract the user's message
                user_message = body.get("messageData", {}).get("textMessageData", {}).get("textMessage", "")

                # Create the response message
                print('user_message')
                print(user_message)
                print('get_gpt_response')
                answer = get_gpt_response(user_message)
                print('answer')
                print(answer)

                # Send the message
                url = "https://7103.api.greenapi.com/waInstance7103166851/sendMessage/39cd5f15b62b42ffa156d1fb589360b4df1d0ed7e56b49a4bf"
                payload = {
                    "chatId": "120363360946946323@g.us",
                    "message": answer
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, json=payload, headers=headers)
                logger.info(f"Message sent, response: {response.text}")
            except Exception as e:
                logger.error(f"Error while processing message: {e}")
                return JSONResponse(content={
                    "status": "Error processing message",
                    "error": str(e),
                    "data": body
                })

        return JSONResponse(content={
            "status": "POST received",
            "data": body
        })

    except Exception as e:
        logger.error(f"Error in handling POST request: {e}")
        return JSONResponse(content={
            "status": "Error handling request",
            "error": str(e)
        })


# Example JSON input
example_json = {
  "typeWebhook": "incomingMessageReceived",
  "instanceData": {
    "idInstance": 7103166851,
    "wid": "972584770076@c.us",
    "typeInstance": "whatsapp"
  },
  "timestamp": 1734783026,
  "idMessage": "3A8F71C92735202948BD",
  "senderData": {
    "chatId": "120363360946946323@g.us",
    "chatName": "ליאורי🏹💕",
    "sender": "972503219900@c.us",
    "senderName": "ליאורי🏹💕",
    "senderContactName": ""
  },
  "messageData": {
    "typeMessage": "textMessage",
    "textMessageData": {
      "textMessage": "הייגירל"
    }
  }
}
