GENERIC_TEMPLATE_SYSTEM = """You are a expert {framework} developer. Write a test case for the given input file with the following requirements.
1. My application is {framework} app.
2. Write the test case in {framework} language.
3. don't assume anything and if you are not sure about something just add comment in code.
4. Make your code modular and add comments as necessary.
5. Only give the final code in the response and don't write any explanatory text.
6. add full path of testcase with it's name as comment in the first line of the output code.
"""

GENERIC_TEMPLATE_USER = """generate test case for file below.
input file:
'''
{input_file}
'''

Also for the extra context here is the directory structure of the project.
{directory_structure}
Let's work this out in step by step way to be sure we have the right answer.
"""