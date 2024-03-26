import json

from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain

from api.predict_v2.ai_helpers.utils import prediction_parser
from config import OPENAI_API_KEY


class ParseChain:
    def __init__(self, ocr_data):
        llm = ChatOpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY, model="gpt-4")

        template = f"""You are an expert 5Para Monitor reader of patients. You are given OCR json data for a 5Para monitor, analyze it and predict patient's reading, you will output the readings in minified JSON format only.
5ParaMonitor OCR data: {json.dumps(ocr_data)}
Tips to analyze the ocr data: monitor can be zoomed in or zoomed out, ocr data is read from left to right of an image from top to bottom(with every row you go down), most of the times readings that we want are at extreme right of the monitor screen, use expertise in reading 5ParaMonitor to make educated guesses about the correct reading of a field.
NOTE: Many fields from below example can be missing, you need to output null for those fields.
Example output in minified JSON format: 
{{"time_stamp":"yyyy-mm-ddThh:mm:ss","ecg":{{"Heart_Rate_bpm":<value/null>}},"nibp":{{"systolic_mmhg":<value/null>,"diastolic_mmhg":<value/null>,"mean_arterial_pressure_mmhg":<value/null>}},"spO2":{{"oxygen_saturation_percentage":<value/null>}},"respiration_rate":{{"breaths_per_minute":<value/null>}},"temperature":{{"fahrenheit":<value/null>}}}}
"""

        system_prompt = PromptTemplate(
            template=template, input_variables=[], template_format="jinja2"
        )
        system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                system_message_prompt,
            ]
        )

        self.chain = LLMChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=True,
        )

    async def async_predict(self):
        prediction = await self.chain.apredict()
        # TODO: add check if prediction is valid json or not
        parsed_prediction = prediction_parser(prediction)
        return parsed_prediction
