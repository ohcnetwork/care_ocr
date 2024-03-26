import json

from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema.messages import HumanMessage

from config import OPENAI_API_KEY
from api.predict_v2.ai_helpers.utils import encode_image, prediction_parser
from api.predict_v2.image_compressor import compress_image_v2


class ParseChainV2:
    def __init__(self, image):
        llm = ChatOpenAI(
            temperature=0.4,
            openai_api_key=OPENAI_API_KEY,
            model="gpt-4-vision-preview",
            max_tokens=4096,
        )

        template = f"""You are an expert 5Para Monitor reader of patients. You are given 5Para Monitor image, analyze it and predict patient's reading, you will output the readings in minified JSON format only.
Tips to analyze the ocr data: monitor can be zoomed in or zoomed out, most of the times readings that we want are at extreme right of the monitor screen, use expertise in reading 5ParaMonitor to make educated guesses about the correct reading of a field.
NOTE: Many fields from below example can be missing, you need to output null for those fields.
Example output in minified JSON format: 
{{"time_stamp":"yyyy-mm-ddThh:mm:ss","ecg":{{"Heart_Rate_bpm":<value/null>}},"nibp":{{"systolic_mmhg":<value/null>,"diastolic_mmhg":<value/null>,"mean_arterial_pressure_mmhg":<value/null>}},"spO2":{{"oxygen_saturation_percentage":<value/null>}},"respiration_rate":{{"breaths_per_minute":<value/null>}},"temperature":{{"fahrenheit":<value/null>}}}}
"""
        image = compress_image_v2(image)
        system_prompt = PromptTemplate(
            template=template, input_variables=[], template_format="jinja2"
        )
        system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)
        human_message = HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_image(image)}",
                        "detail": "high",
                    },
                }
            ]
        )

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                system_message_prompt,
                human_message,
            ]
        )

        self.chain = LLMChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=False,
        )

    async def async_predict(self):
        prediction = await self.chain.apredict()
        print(prediction)
        # TODO: add check if prediction is valid json or not
        parsed_prediction = prediction_parser(prediction)
        return parsed_prediction
