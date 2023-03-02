"""
Access OpenAI for the generation of controlled generation QG outputs.

Author: Anonymous for AIED 2023 LBR Track Submission
"""

import openai

import json
import string
from tqdm import tqdm
import re

LIST_PROMPTS = [
    "remembering",
    "understanding",
    "applying",
    "analyzing",
    "evaluating",
    "creating",
    "beginner",
    "intermediate",
    "advanced"
]

CONTROLLABLE_PROMPT = "Generate {keyword} questions."
EXAMPLE_PROMPT = "\n\nPassage: {example_context}\nQuestion: {example_question}"
GENERATION_PROMPT = "\n\nPassage: {context}\nQuestion:"

class ControlledQG:
    def __init__(
        self,
        key_file_path: str,
        engine: str = "text-davinci-003", # InstructGPT - https://beta.openai.com/docs/models/gpt-3
        temperature: float = 0.7,
        max_tokens: int = 256,
        top_p: float = 1,
        frequency_penalty: float = 1.0,
        presence_penalty: float = 1.0,
        num_samples: int = 1,
    ) -> None:

        file = open(key_file_path, "r")
        key = json.load(file)["key"]
        file.close()
        openai.api_key = key

        self.args = {
            "engine": engine,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        
        self.num_samples = num_samples


    def generate_questions_with_all_prompts(self, context: str, examples: list = []) -> dict:
        """
        Access the OpenAI API and generate questions using the provided context paragraph, (optionally) one or more examples, and each of the question types in LIST_PROMPTS.
        Note that OpenAI is queried self.num_samples of times for each prompt type (default is once).

        :param context: a string holding the source material from which we want to generate questions
        :param examples: a list of dicts holding the example context/question pair for the generation prompt (if empty, then zero-shot prompting)

        :returns: a dictionary of prompt types and the associated generated questions
        """
        all_outputs = {}

        # generate questions for each question type in the list
        for prompt_type in tqdm(LIST_PROMPTS):
            all_outputs[prompt_type] = self.generate_questions(prompt_type, context, examples)

        return all_outputs

    
    def generate_questions(self, prompt_type: str, context: str, examples: list = []) -> dict:
        """
        Access the OpenAI API and generate questions using the provided prompt keyword, context paragraph, and (optionally) examples.
        Note that OpenAI is queried self.num_samples of times for each prompt type (default is once).

        :param prompt_type: a string holding the keyword for controlled QG (see LIST_PROMPTS for full list)
        :param context: a string holding the source material from which we want to generate questions
        :param example: a dict holding the example context/question pair for the generation prompt

        :returns: a list of generated questions
        """
        # some quick checks to see if the example list is OK
        for eg in examples:
            if 'question' not in eg.keys() or 'context' not in eg.keys():
                raise Exception("Example list provided is not in the right format. Should be a list of dicts, where each dict has a 'context' and a 'question'.")

        # format the prompt based on which you are inputting (ie. include examples if one-shot)
        prompt = self.format_prompt(prompt_keyword=prompt_type, context=context, examples=examples)
        args = {"prompt": prompt, **self.args}

        questions = set()
        for _ in range(self.num_samples):
            responses = openai.Completion.create(**args)

            for sample in responses["choices"]:
                questions.add(sample["text"])

        return self.parse_questions(list(set(questions)))


    def format_prompt(self, prompt_keyword: str, context: str, examples: list = []):
        """
        Helper function to format the prompt with provided keyword, context, and example(s).

        :param prompt_keyword: a str containing the keyword for controllable generation
        :param context: a string containg the context we want to use for generation
        :param examples: a list of dictionaries containing the keys 'context' and 'question' (can be an empty list for zero-shot)

        :returns: the formatted prompt
        """
        prompt = CONTROLLABLE_PROMPT.format(keyword=prompt_keyword)
        
        # iterate over all provided examples (could be 0) and add to the prompt
        for example in examples:
            prompt += EXAMPLE_PROMPT.format(example_context=example['context'], example_question=example['question'])

        prompt += GENERATION_PROMPT.format(context=context)

        return prompt


    def parse_questions(self, question_lists: list) -> list:
        """
        Parsing the one string outputs from querying OpenAI into a list of questions. Also removes any strings that are too short to be questions.

        :param question_lists: the unprocessed string of questions from the generation function
        :returns: a list of individual questions as opposed to a list of self.num_sample outputs
        """
        # note that len(question_lists) should be self.num_samples (ie. number of times we query OpenAI)
        sublist = []
        for sample in question_lists:
            sublist.extend(sample.split("\n"))

        # simple preprocessing on all questions
        sublist = [self.preprocess_question(q) for q in sublist]

        # remove any empty/too small strings
        sublist = [s for s in sublist if len(s) > 10]

        # remove any 'Question: ' prefixes from the generations
        sublist = [s.replace("Question:", "").strip() for s in sublist]

        # remove True/False from the end of generations (edge case seen with TF questions in the zero-shot paradigm where InstructGPT tries to answer)
        for i in range(len(sublist)):
            if sublist[i][-4:].lower() == 'true':
                sublist[i] = sublist[i][:-4].strip()
            if sublist[i][-5:].lower() == 'false':
                sublist[i] = sublist[i][:-5].strip()

        # remove any incomplete sentences
        sublist = [s for s in sublist if s[-1] in list(string.punctuation)]

        # remove any attempted answers (i.e. if it contains 'Answer:') - seen in the zero shot paradigm
        sublist = [s for s in sublist if 'Answer:' not in s]

        return sublist

    
    def preprocess_question(self, question: str) -> str:
        """
        Simple preprocessing of each question. Removes bullets/enumeration.

        :param question: a str holding the question to process
        :returns: a processed question
        """

        # remove enumeration from questions (e.g., 1., 2), C., ...)
        question = question.strip() # to remove leading whitespaces

        question = re.sub("^[0-9]\\.", "", question)
        question = re.sub("^[0-9]\\) ", "", question)
        question = re.sub("^\\*", "", question)
        question = re.sub("^[:upper:]\\.", "", question)
        question = re.sub("^[-]", "", question)

        # remove any new leading whitespaces
        question = question.strip()

        return question
