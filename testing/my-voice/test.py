# Import the library dynamically
# mysp=__import__("my-voice-analysis") 

import service.myVoiceAnalysis as mysp



name="record_out" # Audio File title
path=r'D:/MyGitRepo/testing/vc' 

obj = mysp.MyVoiceAnalysis('audio/record_out.wav')
# print(obj.number_of_pauses())
# print(obj.number_of_syllables())
# print(obj.rate_of_speech())

# for i in obj.get_function_list():
#     print(i)

obj.total()#mysp.mysptotal(p,c)
obj.gender_mode_of_speech()#mysp.myspgend(p,c)
obj.number_of_syllables()#mysp.myspsyl(p,c)
obj.number_of_pauses()#mysp.mysppaus(p,c)
obj.rate_of_speech()#mysp.myspsr(p,c)
obj.articulation_rate()#mysp.myspatc(p,c)
obj.speaking_duration()#mysp.myspst(p,c)
obj.original_duration()#mysp.myspod(p,c)
obj.balance()#mysp.myspbala(p,c)
obj.myspf0mean()#mysp.myspf0mean(p,c)
obj.myspf0sd()#mysp.myspf0sd(p,c)
obj.myspf0med()#mysp.myspf0med(p,c)
obj.myspf0min()#mysp.myspf0min(p,c)
obj.myspf0max()#mysp.myspf0max(p,c)
obj.myspf0q25()#mysp.myspf0q25(p,c)
obj.myspf0q75()#mysp.myspf0q75(p,c)
obj.pronunciation_posteriori_probability_score_percentage()#mysp.mysppron(p,c)












