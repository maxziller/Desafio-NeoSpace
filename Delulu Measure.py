import os
from openai import OpenAI



#Need to place API_KEY in here
OPENAI_KEY = 
client = OpenAI(api_key = OPENAI_KEY)


#Function to call ChatGPT 4o to answer the prompt
def answer(question):
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": question,
        }],
        model="gpt-3.5-turbo",
    )

    return(chat_completion.choices[0].message.content)


#Function that decides if the answer is right or not
#Return 0 if hallucination, 1 if proper answer
def correcting(proper_answer, given_answer):
    question  = "Are both following texts agreeing? If they do, answer just with a 1. If they don't, answer just with a 0 without any punctuation. First text: "
    question += proper_answer
    question += " Second text: "
    question += given_answer
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": question,
        }],
        model="gpt-3.5-turbo",
    )

    a = chat_completion.choices[0].message.content
    print(a)
    return a


#Dictionary to receive all the TestInput objects with the questions and proper answers
ModelQuestions = dict()
with open("Ideal Answers.csv","r", encoding = "utf8") as ideal_answers:
    
    for line in ideal_answers:
        temp = line.strip()
        temp = temp.split(";")
        ques = temp[0]
        ans = temp[1]
        ModelQuestions[ques] = ans


#Funcion made for calculating the hallucination tax in %
with open("Wrong Answers.csv","r", encoding = "utf8") as testing_llm:
#with open("Random Answers.csv","r", encoding = "utf8") as testing_llm:
    hallucination = 0
    questions = 0
    for line in testing_llm:
        temp = line.strip()
        temp = temp.split(";")
        ques = temp[0]
        ans = temp[1]
        questions += 1
        hallucination += int(correcting(ModelQuestions[ques],ans))
    print(1.0 - float(hallucination)/float(questions))


'''
#Functions used on building the answer files
with open("Random Answers.csv","w", encoding = "utf8") as wrong_llm:
#with open("Wrong Answers.csv","w", encoding = "utf8") as wrong_llm:    

    for k in ModelQuestions.keys():
        
        #newQuestion = k + " Give me a very wrong answer."
        newQuestion = k + " Throw a coin and, if it's heads, give me the correct answer, if it's tails, give me a wrong answer. Never warn me if the answer is right or wrong and don't tell me which side of the coin you had."
        wrongAnswer = answer(newQuestion)
        wrong_llm.write(k)
        wrong_llm.write(";")
        wrong_llm.write(wrongAnswer)
        wrong_llm.write("\n")

'''
