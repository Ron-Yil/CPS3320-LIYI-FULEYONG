This speech recognition program calls iFLYtek voice dictation, uses Python to realize speech recognition, and converts real-time speech into text.

Before running the file, you need to complete the plug-in download：


Py files are get_audio. Py and iat_demo.py. Audios folder is created to store the recording file input.wav.The entire file directory is as follows:

asr_SDK(文件名)
├─ Readme.html
├─ audios
│    └─ input.wav（存放音频）
├─ bin
│    ├─ gm_continuous_digit.abnf
│    ├─ ise_cn
│    ├─ ise_en
│    ├─ msc
│    ├─ msc.dll （因为我是32位的python，所以用的这个动态链接库）
│    ├─ msc_x64.dll
│    ├─ source.txt
│    ├─ userwords.txt
│    └─ wav
├─ doc
├─ get_audio.py
├─ iat_demo.py
├─ include
├─ libs
├─ release.txt
└─ samples

After completing the above steps, we start debugging two Python code files:

1. Recording
pyaudio is used for recording, you need to download the relevant wheels. The get_audio.py file is used to save the recorded voice into to the audios file.

The recording is kept in a loop, and each time it is re-recorded, the previous audio is overwritten.

2. Speech recognition
Directly using the Voice dictation web API of IFLYTEK official website on Python example, on this basis, relevant adjustments are made to automatically recognize the recording into text.
The iat_demo.py file is used to recognize the recorded voice.

3. Start the program

In the program folder, right-click iat_demo and select Edit with IDLE- >. Edit with IDLE3.7(32 bit) open, then use F5 quick boot. 



4. Reference
All the links below are references for our team when developing this software.

This URL can help users to download the API SDK from the website:
https://blog.csdn.net/cxyuanba/article/details/106929405?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165354803216781432933040%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165354803216781432933040&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-1-106929405-null-null.142^v10^control,157^v12^control&utm_term=%E5%A6%82%E4%BD%95%E8%B0%83%E7%94%A8%E7%A7%91%E5%A4%A7%E8%AE%AF%E9%A3%9Eapi&spm=1018.2226.3001.4187

This URL can help users to install the wheel pyaudio without error:
https://blog.csdn.net/sueRimn/article/details/98500352

This URL is the API download webiste--科大讯飞：
https://www.xfyun.cn/doc/asr/rtasr/API.html
