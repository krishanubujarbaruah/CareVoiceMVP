import time
from flask import Flask, Response, jsonify, render_template, request ,redirect, url_for
from response import *
from memory import *
from prompts import *
from langchainAISearch import *



app = Flask(__name__)


assistant_memory = Memory([])
assistant_memory.add_system_message(system_prompt("Dr. Patil"))
assistant_memory.add_doctor_message('''Introduction session and intial information . 
                          Ask patient as many questions you can to guage the intial situation and 
                          level of emergency on patients side .
                          End the conversation with thank you when enough 10-15 questions are asked.''')
assistant_memory.add_assistant_message('''Can you please state your name and age for the record?''' )
# Define the default route to return the index.html file

knowmore_memory = Memory([])
knowmore_memory.add_system_message(hc_assistant_prompt())
knowmore_memory.add_assistant_message('''Come on !! ask me anything about healthcare practices so that you live a healthy life !!!!  ''' )

messages = []




@app.route("/")
def home():
    return render_template("index.html",)



@app.route("/assistant")
def assistant():
    # assistant_memory.print_chat()
    chats=assistant_memory.get_chats()
    return render_template("assistant.html",doctor_name="DR.Patil",chats=chats)


# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    # print(message)
    
    chats=assistant_memory.add_patient_message(message)
    # memory.print_chat()
    resp=get_response(chats)
    # print(resp)
    chats=assistant_memory.add_assistant_message(resp['content'])
    return resp


@app.route("/knowmorepage")
def knowmorepage():
    # assistant_memory.print_chat()
    chats=knowmore_memory.get_chats()
    return render_template("knowmore_page.html",chats=chats)

@app.route("/knowmore", methods=["POST"])
def knowmore():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    # print(message)
    resp=get_response_from_docs(message)
    # print(resp)
    return resp


@app.route("/doctor")
def doctor():
    return render_template("doctor.html",doctor_name="DR.Patil")


@app.route("/moreinfopage")
def moreinfopage():
    return render_template("get_more_info.html")

@app.route("/prescriptionpage")
def prescriptionpage():
    return render_template("prescription_page.html")

@app.route("/suggestionpage")
def suggestionpage():
    return render_template("suggestion_page.html")


@app.route("/summary", methods=["GET"])
def summary():
    chats=assistant_memory.get_chats()
    summary=get_summary(chats)

    return summary

@app.route("/moreinfo", methods=["POST"])
def moreinfo():
    # Receive the message
    info_message = request.json.get('message')
    # print(info_message)
    # Append the message to the global list of messages
    chats=assistant_memory.add_doctor_message(info_message)
    # assistant_memory.print_chat()
    resp=get_response(chats)
    message=resp['content']
    chats=assistant_memory.add_assistant_message(resp['content'])
    if message:  # Make sure the message is not empty
        messages.append(message)
    return jsonify(success=True)

@app.route("/prescription", methods=["POST"])
def precription():
    # Receive the message
    info_message = request.json.get('message')
    # print(info_message)
    # Append the message to the global list of messages
    chats=assistant_memory.add_doctor_prescription_message(info_message)
    # assistant_memory.print_chat()
    resp=get_response(chats)
    message=resp['content']
    chats=assistant_memory.add_assistant_message(resp['content'])
    if message:  # Make sure the message is not empty
        messages.append(message)
    return jsonify(success=True)

@app.route("/suggestion", methods=["POST"])
def suggestion():
    # Receive the message
    info_message = request.json.get('message')
    # print(info_message)
    # Append the message to the global list of messages
    chats=assistant_memory.add_doctor_suggestion_message(info_message)
    # assistant_memory.print_chat()
    resp=get_response(chats)
    message=resp['content']
    print(message)
    chats=assistant_memory.add_assistant_message(resp['content'])
    if message:  # Make sure the message is not empty
        messages.append(message)
    return jsonify(success=True)


def stream():
    if messages:
        # Yield the last message in the stream
        last_message = messages.pop()  
        yield f"data: {last_message }\n\n"
        time.sleep(1)  # Prevent the function from ending immediately

@app.route("/stream")
def stream_messages():
    return Response(stream(), mimetype="text/event-stream")
    


@app.route("/reset", methods=["GET"])
def reset():
    # Receive the message
    # info_message = request.json.get('message')
    assistant_memory.reset_memory()
    assistant_memory.add_system_message(system_prompt("Dr. Patil"))
    assistant_memory.add_doctor_message('''Introduction session and intial information . 
                            Ask patient as many questions you can to guage the intial situation and 
                            level of emergency on patients side .
                            End the conversation with thank you when enough 10-15 questions are asked.''')
    assistant_memory.add_assistant_message('''Can you please state your name and age for the record?''' )
    # assistant_memory.print_chat()
    return jsonify(success=True)

if __name__=='__main__':
    app.run()

