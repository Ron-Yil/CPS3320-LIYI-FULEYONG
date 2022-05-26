import websocket
import datetime
import hashlib
import base64
import hmac
import json
import os, sys
from urllib.parse import urlencode
import logging
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from pyaudio import PyAudio,paInt16
from get_audio import get_audio # import recoding

input_filename = "input.wav"               # Microphone acquisition of voice input
input_filepath = "./audios/"              # Enter the path of the file
in_path = input_filepath + input_filename

type = sys.getfilesystemencoding()

path_pwd = os.path.split(os.path.realpath(__file__))[0]
os.chdir(path_pwd)

try:
    import thread
except ImportError:
    import _thread as thread

logging.basicConfig()

STATUS_FIRST_FRAME = 0  # The identity of the first frame
STATUS_CONTINUE_FRAME = 1  # Intermediate frame identification
STATUS_LAST_FRAME = 2  # The identity of the last frame

framerate = 8000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 2

global wsParam

class Ws_Param(object):

    def __init__(self, host):
        self.Host = host
        self.HttpProto = "HTTP/1.1"
        self.HttpMethod = "GET"
        self.RequestUri = "/v2/iat"
        self.APPID = "5d312675"
        self.Algorithm = "hmac-sha256"
        self.url = "wss://" + self.Host + self.RequestUri

        # Audio recording collection
        get_audio("./audios/input.wav")

        # Set up the test audio file
        self.AudioFile = r"./audios/input.wav"

        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {"domain":"iat", "language": "zh_cn","accent":"mandarin"}

    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        APIKey = 'a6aabfcca4ae28f9b6a448f705b7e432' # Get APIKey
        APISecret = 'e649956e14eeb085d1b0dce77a671131' # Get APISecret

        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        signature_sha = hmac.new(APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        url = url + '?' + urlencode(v)
        return url


def on_message(ws, message):
    msg = json.loads(message) # Convert JSON objects to Python objects. Convert JSON formats to dictionary formats
    try:
        code = msg["code"]
        sid = msg["sid"]

        if code != 0:
            errMsg = msg["message"]
            print("sid:%s call error:%s code is:%s\n" % (sid, errMsg, code))
        else:
            result = msg["data"]["result"]["ws"]
            data_result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')) 
            print("sid:%s call success!" % (sid))
            print("result is:%s\n" % (data_result))
    except Exception as e:
        print("receive msg,but parse exception:", e)

# A Websocket error was received
def on_error(ws, error):
    print("### error:", error)

# Received a webSocket down message
def on_close(ws):
    print("### closed ###")

# Received a webSocket connection setup message
def on_open(ws):
    def run(*args):
        frameSize = 1280  # The audio size of each frame
        intervel = 0.04  # Audio interval
        status = STATUS_FIRST_FRAME  # The state of the audio, identifying whether the audio is the first frame, the middle frame, or the last frame
        with open(wsParam.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)

                if not buf:
                    status = STATUS_LAST_FRAME
                # Frame 1 processing
                if status == STATUS_FIRST_FRAME:

                    d = {"common": wsParam.CommonArgs,
                         "business": wsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                   "audio": str(base64.b64encode(buf),'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # Intermediate frame processing
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                   "audio": str(base64.b64encode(buf),'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # Last frame processing
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf),'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    wsParam = Ws_Param("ws-api.xfyun.cn")
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

