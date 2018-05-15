# RaspberryPi_VOICE_V1
基于百度语音的在线合成语音，整点播报语音系统，天气预报，网站新闻播报，提醒事项等

crontab设置


30 7 * * * mpv /home/pi/Desktop/music/*.mp3    #每天7.30播放歌曲、、 （可以尝试换成网络收音机）



0  7-22 * * * python3 /home/pi/Desktop/voice/weat.py #每天7点到网上10点 播报天气等

