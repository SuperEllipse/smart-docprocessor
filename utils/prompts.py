# from smartdoc_utils import (
#     model_output,
#     model_output_1,
#     model_input,
#     model_input_1,
#     model_input_2,
#     model_output_2,
#     model_input_3,
#     model_output_3
# )
model_input = """
'I saw a    sample prodcut.  These product are below expeccted quality. I start to underdstand what he said is quite right. The correct valu is 12.5%% and 3rd postion. The time is 10:30am. The length of the object is 845mm and costs $1million. The sunise happens at 0750 EST and visibilty is 35 km. The right way too sumize and favor some advisor's is still to be found.'"""
# The text generated by the KAREN model
model_output = """
1. Edited Text: 'I saw a sample product. These products are below expected quality. I started to understand what he said is quite right. The correct value is 12.5%% and 3rd position. The time is 10:30 am. The length of the object is 845mm and costs $1m. The sunrise happens at 0750 EST and visibility is 35 km. The right way to summarize and favor some advisors' is still to be found.'
2. Corrections:
   a) Removed extra spaces after 'I saw' and before 'These products are below expected quality.'
   b) Changed 'sample prodcut' to 'sample product.'
   c) Corrected the tense from 'start' to 'started'
   d) Corrected the spelling of 'expeccted quality.' to 'expected quality.'
   e) Fixed the spelling "correct valu" to 'correct value.'
   f) Fixed the time format to '10:30 am.'
   g) Abbreviated '$1million' to '$1m.'
   h) Corrected 'sunise' to 'sunrise.'
   i) Fixed the spelling of'visibilty' to 'visibility.'
   j) Corrected 'too sumize' to 'to summarize.'
   k) Fixed punctuation in 'advisor's' to 'advisors'.
"""

model_input_1 = """
'I read a article about new technology. These technologie are not very impresssive. I think the points he made are mostly valid. The value should be 15.3%% and in 2nd postion. The time is 9:45am. The object's width is 732cm and priced at $500,000. The moonrise occured at 0635 UTC and the visibility range is 40 miles. The correct strategy for optimizing results and consulting a specialist's insights remains unclear.'
"""
model_output_1 = """
1. Edited Text: 'I read an article about new technology. These technologies are not very impressive. I think the points he made are mostly valid. The value should be 15.3%% and in 2nd position. The time is 9:45 am. The object's width is 732cm and priced at $500,000. The moonrise occurred at 0635 UTC and the visibility range is 40 miles. The correct strategy for optimizing results and consulting a specialist's insights remains unclear.'

2. Corrections: 
   a) Changed 'I read a article' to 'I read an article.' 
   b) Corrected spelling of 'technologie' to 'technologies.' 
   c) Fixed spelling of 'impresssive' to 'impressive.' 
   d) Corrected spelling of 'postion' to 'position.' 
   e) Changed the time format to '9:45 am.'  
   f) Updated 'priced at $500,000' for clarity and consistency. 
   g) Corrected spelling of 'occured' to 'occurred.' 
   h) Replaced 'visibility is 40 miles' to 'visibility range is 40 miles.' 
   i) Clarified 'correct strategy for optimizing results and consulting a specialist's insights remains unclear.'
"""

model_input_2 = """
'I have a book called "The Sun Also Rises". The book is about a group of American and British expatriates who travel from Paris to Pamplona to watch the running of the bulls and the bullfights. The book was published in 1926 and was written by Ernest Hemingway. The main characters are Jake Barnes, Lady Brett Ashley, Robert Cohn, and Pedro Romero. The book is considered one of Hemingway's masterpieces and is a classic of American literature.'
"""

model_output_2 = """
1. Edited Text: 'I have a book called "The Sun Also Rises". The book is about a group of American and British expatriates who travel from Paris to Pamplona to watch the running of the bulls and the bullfights. The book was published in 1926 and was written by Ernest Hemingway. The main characters are Jake Barnes, Lady Brett Ashley, Robert Cohn, and Pedro Romero. The book is considered one of Hemingway's masterpieces and is a classic of American literature.'

2. Corrections: None
"""


model_input_3 = """
'Jack and Jill went up the hill to fetch a pail of water'
"""

model_output_3 = """
1. Edited Text: 'Jack and Jill went up the hill to fetch a pail of water'

2. Corrections: None
"""

model_input_3 = """
'Ministry of Defence Industries, Secretary, Associate Secretary: CAPT John Lenon is leading the team with 8 tanks along with CMDR Jack Sparrow on 12 Dec 13. The ACM of the western front of the ADF is keenly interested in this project.'
"""

model_output_3 = """
1. Edited Text: 'MINDI, SEC, ASSOCSEC: Captain John Lenon is leading the team with eight Tanks along with Commander Jack Sparrow leadership on 12 December 2013. The Air Chief Marshall of the Australian Defence Force is keenly interested in this Project.'

2. Corrections:
    a) Use acronym MINDI for  Ministry of Defence Industries
    b) Use acronym SEC for Secretary 
    c) Use acronym ASSOCSEC for Associate Secretary 
    a) Changed the acronym in CAPT John Lenon to Captain John Lenon
    b) Changed the acronym in CMDR Jack Sparrow to Commander Jack Sparrow
    f) Changed the 8 tanks to the word eight Tanks
    c) Changed 12 Dec 13 to 12 December 2013 as the date needs to be fully expanded
    c) Changed the acronym in ACM of the western front  to Air Chief Marshall  of the western front
    d) Changed the acronym in ADF is keenly interested to Australian Defence Force is keenly interested 
    e) Changed Ministry of Defence Industries to MINDI
"""




karen_system_prompt = "You are an expert editor who corrects spelling, formatting and grammatical errors\n"

karen_prompt = (
    "** TASK **\n"
    "\n------------------------------------------------------------\n"
    "Example 1."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input}\n"
    f"{model_output}"
    "\n------------------------------------------------------------\n"
    "Example 2."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input_1}\n"
    f"{model_output_1}"
    "\n------------------------------------------------------------\n"
    "Example 3."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input_2}\n"
    f"{model_output_2}"
    "\n------------------------------------------------------------\n"
    "Example 4."
    "\n------------------------------------------------------------\n"    
    f"\nText: {model_input_3}\n"
    f"{model_output_3}"
    "\n------------------------------------------------------------\n"   
    "Only focus on the text after this. \n"
    "1. Edit the following text for spelling and grammar mistakes: "
    "'{text}'\n"
    "2. Remove any formatting errors such as extra spaces. \n"
    "\n**IMPORTANT**\nUse the following template to format your response."
    "1. Edited Text: \n"
    "{{ Your corrected text here, blank if nothing is edited }}\n"
    "2. Corrections: \n"
    "{{ Make a numbered list of your corrections, blank if no corrections are there }}\n\n"
    "Do not make up your own template. Use the one provided above."
)

llama_system_prompt = (
    "You are an expert editor who corrects spelling, formatting and grammatical errors. "
    "**RULES**\n"
    "* Analyze the text before editing it. \n"
    "* Follow British English spelling and grammar rules. Do not use American English. \n"
    "* Please fix all spelling mistakes, punctuation errors, and grammatical errors. \n"
    "* Do not correct or expand any abbrieviations or acronyms you do not know about. \n"
    "* Do not rename any names or proper nouns. Capitalise the initials if "
    "needed, but do not rename names like aircraft names, base names, locations etc. \n"
    "* Do not assume anything, if you're confused, leave it as it is. \n"
    "* Do not add new information. Only refer to the text provided. "
    "For example, do not add dates or months "
    "if they are not filled. \n"
    "* Remove any formatting errors such as extra spaces. \n"
    "* Format phone numbers in Australian Format. \n"
    "\n**IMPORTANT**\nUse the following template to format your response."
    "1. Edited Text: \n"
    "{ Your corrected text here, blank if nothing is edited }\n"
    "2. Corrections: \n"
    "{ Make a numbered list of your corrections, blank if no corrections are there }\n\n"
    "Do not make up your own template. Use the one provided above. "
    "If there are no edits or corrections, return: \n\n1. Edited Text: \n2. Corrections:"
)

llama_prompt = (
    "Use the following examples as reference for editing.\n"
    "\n------------------------------------------------------------\n"
    "Example 1."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input}\n"
    f"{model_output}"
    "\n------------------------------------------------------------\n"
    "Example 2."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input_1}\n"
    f"{model_output_1}"
    "\n------------------------------------------------------------\n"
    "Example 3."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input_2}\n"
    f"{model_output_2}"
    "\n------------------------------------------------------------\n"
    "Example 4."
    "\n------------------------------------------------------------\n"  
    f"\nText: {model_input_3}\n"
    f"{model_output_3}"
    "\n------------------------------------------------------------\n"       
    "Following is the text you have to edit: "
    "\n------------------------------------------------------------\n"
    "\n"
    "Text: '{text}'\n"
    "\n"
    ""
)

gemma_prompt = (
    "You are an expert editor who corrects spelling, formatting and grammatical errors. "
    "**RULES**\n"
    "* Analyze the text before editing it. \n"
    "* Follow British English spelling and grammar rules. Do not use American English. \n"
    "* Fix spelling mistakes, punctuation errors, and grammatical errors. \n"
    "* Do not correct or expand any abbrieviations or acronyms you do not know about. \n"
    "* Do not rename any names or proper nouns. Capitalise the initials if "
    "needed, but do not rename names like aircraft names, base names, locations etc. \n"
    "* Do not assume anything, if you're confused, leave it as it is. \n"
    "* Do not add new information. Only refer to the text provided. "
    "For example, do not add dates or months "
    "if they are not filled. \n"
    "* Remove any formatting errors such as extra spaces. \n"
    "* Format phone numbers in Australian Format. \n"
    "\n**IMPORTANT**\nUse the following template to format your response."
    "1. Edited Text: \n"
    "{{ Your corrected text here, blank if nothing is edited }}\n"
    "2. Corrections: \n"
    "{{ Make a numbered list of your corrections, blank if no corrections are there }}\n\n"
    "Do not make up your own template. Use the one provided above."
    "If there are no edits or corrections, return: \n\n1. Edited Text: \n2. Corrections:"
    "\n"
    "\n------------------------------------------------------------\n"
    "Example 1."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input}\n"
    f"{model_output}"
    "\n------------------------------------------------------------\n"
    "Example 2."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input_1}\n"
    f"{model_output_1}"
    "\n------------------------------------------------------------\n"
    "Example 3."
    "\n------------------------------------------------------------\n"
    f"\nText: {model_input_2}\n"
    f"{model_output_2}"
    "\n------------------------------------------------------------\n"
    "Example 4."
    "\n------------------------------------------------------------\n"    
    f"\nText: {model_input_3}\n"
    f"{model_output_3}"
    "\n------------------------------------------------------------\n"       
    "Following is the text you have to edit: "
    "\n------------------------------------------------------------\n"
    "\n"
    "Text: '{text}'\n"
    "\n"
)
