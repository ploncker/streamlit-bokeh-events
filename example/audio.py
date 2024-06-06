"""
Created on Fri Jun  7 09:09:00 2024

@author: ross

uses webkit
https://developer.chrome.com/blog/voice-driven-web-apps-introduction-to-the-web-speech-api
source
https://discuss.streamlit.io/t/speech-to-text-on-client-side-using-html5-and-streamlit-bokeh-events/7888
github
https://github.com/ash2shukla/streamlit-bokeh-events/blob/master/example/custom_js.py
"""
# import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS

# text = st.text_input("Say what ?")

# tts_button = Button(label="Speak", width=100)

# tts_button.js_on_event("button_click", CustomJS(code=f"""
#     var u = new SpeechSynthesisUtterance();
#     u.text = "{text}";
#     u.lang = 'en-US';

#     speechSynthesis.speak(u);
#     """))

# st.bokeh_chart(tts_button)


import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        
