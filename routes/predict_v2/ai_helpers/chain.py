import json

from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain import PromptTemplate, LLMChain

from base import OPENAI_API_KEY


class ChatChain:
    def __init__(self, ocr_data):
        llm = ChatOpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY, model="gpt-4")

        template = f"""You are an OCR to JSON converter for 5ParaMonitor. You are given ocr json data for a 5 Para monitor, analyze the brand and predict patients reading, you will output the readings in JSON format.
5ParaMonitor OCR data: {json.dumps(ocr_data)}
Tips to analyze the ocr data: monitor can be zoomed in or zoomed out, ocr data is read from left to right of an image from top to bottom(with every row you go down), most of the times readings that we want are at extreme right of the monitor screen, there can be params like spo2, temp, bp etc present in ocr data, use them to your benefits and identify the correct value, temperature is always a decimal value, don't repeat a single value for multiple params, if you are not sure about a value, you can answer it as null, use common sense to get the correct field of a value.
Example output: 
{{"spo2": "value/null", "resp": "value/null", "temperature": "value/null", "pulse":"value/null", "bp":"value/null"}}
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

        parsed_prediction = json.loads(prediction)
        return parsed_prediction
