from flask import Flask,request,render_template
import replicate
import os
import time
from openai import OpenAI

openai_api_key=os.getenv（"OPENAI_API_TOKEN"）
os.environ["REPLICATE_API_TOKEN"]="r8_2idkAutIh1jCAVVRIbEDgqt9zNUdbhG2cS1AF"

model=OpenAI(api_key=openai_api_key)

app = Flask(__name__)

r = ""
first_time = 1

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global r,first_time
    if first_time==1:
        r = request.form.get("r")
        first_time=0
    return(render_template("main.html",r=r))

@app.route("/test_gpt",methods=["GET","POST"])
def test_gpt():
    return(render_template("test_gpt.html"))

@app.route("/test_result",methods=["GET","POST"])
def test_result():
    q = request.form.get("q")
    r = model.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {
            "role" : "user"
            "content" : q
        }
    ]
    )
    time.sleep(5)
    return(render_template("text_result.html",r=r.choices[0].message.content))

@app.route("/image_gpt",methods=["GET","POST"])
def image_gpt():
    return(render_template("image_gpt.html"))

@app.route("/image_result",methods=["GET","POST"])
def image_result():
    q = request.form.get("q")
    r = replicate.run(
    "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
    input={
        "prompt": q,
        }
    )

@app.route("/end",methods=["GET","POST"])
def end():
    global first_time,r
    first_time = 1
    return(render_template("end.html",r=r))

if __name__ == "__main__":
    app.run()
