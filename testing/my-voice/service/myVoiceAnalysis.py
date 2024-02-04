from parselmouth.praat import call, run_file
import inspect
import types
import pandas as pd
import numpy as np
from scipy.stats import binom
from scipy.stats import ks_2samp
from scipy.stats import ttest_ind
import os
import shutil
from praatio.textgrid import openTextgrid
from praatio.data_classes import point_tier, interval_tier

class MyVoiceAnalysis:

    PRAAT_SCRIPT = "myspsolution.praat"
    CURRENT_PRAAT_SCRIPT = os.path.join(os.path.dirname(os.path.realpath(__file__)), PRAAT_SCRIPT)

    def __init__(self, file_path: str) -> None:

        self.directory, self.sound_name = os.path.split(file_path)
        self.text_grid = self.sound_name.split('.')[0] + ".TextGrid"
        self.running_file_path = os.getcwd()

        try:
            # As run_file from parselmout take working director path by default so has to copy stuff to working temporary
            input_file_dest = os.path.join(self.running_file_path, self.sound_name)
            shutil.copyfile(file_path, input_file_dest)

            praat_script_dest = os.path.join(self.running_file_path, MyVoiceAnalysis.PRAAT_SCRIPT)
            shutil.copyfile(MyVoiceAnalysis.CURRENT_PRAAT_SCRIPT, praat_script_dest)

            # Running the analysis using run_file method
            self.objects: tuple = run_file(
                MyVoiceAnalysis.PRAAT_SCRIPT, -20, 2, 0.3, "yes",
                self.sound_name, self.directory, 80, 400, 0.01,
                capture_output=True
            )

        except Exception:
            raise FileNotFoundError("File may be missing or No Voice Detected")
        finally:
            # Deleting the copied files
            #shutil.copyfile(MyVoiceAnalysis.CURRENT_PRAAT_SCRIPT, praat_script_dest)
            os.remove(input_file_dest)
            os.remove(praat_script_dest)

    def point_tier_dataframe(self):
        textgrid_file = os.path.join(self.directory, self.text_grid)
        tg = openTextgrid(textgrid_file, includeEmptyIntervals=True)
        tier_names = tg.tierNames

        # Create empty DataFrame for PointTiers
        point_tier_df = pd.DataFrame()

        # Iterate through each PointTier in the TextGrid
        for tier_name in tier_names:
            tier = tg._tierDict[tier_name]

            # Extract information from PointTier
            if isinstance(tier, point_tier.PointTier):
                tier_data = [(point[0], point[1]) for point in tier.entries]
                tier_df = pd.DataFrame(tier_data, columns=[f"{tier_name}_number", f"{tier_name}_mark"])

                # Concatenate with the PointTier DataFrame
                point_tier_df = pd.concat([point_tier_df, tier_df], axis=1)

        # Sort DataFrame by the first column
        point_tier_df = point_tier_df.sort_values(by=point_tier_df.columns[0]).reset_index(drop=True)

        return point_tier_df

    def interval_tier_dataframe(self):
        textgrid_file = os.path.join(self.directory, self.text_grid)
        tg = openTextgrid(textgrid_file, includeEmptyIntervals=True)
        tier_names = tg.tierNames

        # Create empty DataFrame for IntervalTiers
        interval_tier_df = pd.DataFrame()

        # Iterate through each IntervalTier in the TextGrid
        for tier_name in tier_names:
            tier = tg._tierDict[tier_name]

            # Extract information from IntervalTier
            if isinstance(tier, interval_tier.IntervalTier):
                tier_data = [(interval[0], interval[1], interval[2]) for interval in tier.entries]
                tier_df = pd.DataFrame(tier_data, columns=[f"{tier_name}_xmin", f"{tier_name}_xmax", f"{tier_name}_text"])

                # Concatenate with the IntervalTier DataFrame
                interval_tier_df = pd.concat([interval_tier_df, tier_df], axis=1)

        # Sort DataFrame by the first column
        interval_tier_df = interval_tier_df.sort_values(by=interval_tier_df.columns[0]).reset_index(drop=True)

        return interval_tier_df

    def number_of_syllables(self):
        z3:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[0]) # will be the integer number 10
            z4=float(z2[3]) # will be the floating point number 8.3
            print ("number_ of_syllables=",z3)
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z3
    
    def number_of_pauses(self):
        z3: int = 0
        try:
            print(self.objects[0])
            z1 = str(self.objects[1])
            z2 = z1.strip().split()
            z3 = int(z2[1])
            z4 = float(z2[3])
            print("number_of_pauses=", z3)
        except Exception as e:
            print(e)
            print("Try again; the sound of the audio was not clear")
        return z3

    def rate_of_speech(self):
        z3: int=0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[2]) # will be the integer number 10
            z4=float(z2[3]) # will be the floating point number 8.3
            print ("rate_of_speech=",z3,"# syllables/sec original duration")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z3

    def articulation_rate(self):
        z3:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[3]) # will be the floating point number 8.3
            print ("articulation_rate=",z3,"# syllables/sec speaking duration")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z3

    def speaking_duration(self):
        z4:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[4]) # will be the floating point number 8.3
            print ("speaking_duration=",z4,"# sec only speaking duration without pauses")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z4

    def original_duration(self):
        z4:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[5]) # will be the floating point number 8.3
            print ("original_duration=",z4,"# sec total speaking duration with pauses")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z4

    def balance(self):
        z4:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[6]) # will be the floating point number 8.3
            print ("balance=",z4,"# ratio (speaking duration)/(original duration)")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z4

    def myspf0mean(self):
        z4:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[7]) # will be the floating point number 8.3
            print ("f0_mean=",z4,"# Hz global mean of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z4

    def myspf0sd(self):
        z4:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[8]) # will be the floating point number 8.3
            print ("f0_SD=",z4,"# Hz global standard deviation of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z4

    def myspf0med(self):
        z4:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[3]) # will be the integer number 10
            z4=float(z2[9]) # will be the floating point number 8.3
            print ("f0_MD=",z4,"# Hz global median of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z4

    def myspf0min(self):
        z3:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[10]) # will be the integer number 10
            z4=float(z2[10]) # will be the floating point number 8.3
            print ("f0_min=",z3,"# Hz global minimum of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear") 
        return z3

    def myspf0max(self):
        z3:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[11]) # will be the integer number 10
            z4=float(z2[11]) # will be the floating point number 8.3
            print ("f0_max=",z3,"# Hz global maximum of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z3

    def myspf0q25(self):
        z3:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[12]) # will be the integer number 10
            z4=float(z2[11]) # will be the floating point number 8.3
            print ("f0_quan25=",z3,"# Hz global 25th quantile of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z3

    def myspf0q75(self):
        z3:int = 0
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[13]) # will be the integer number 10
            z4=float(z2[11]) # will be the floating point number 8.3
            print ("f0_quan75=",z3,"# Hz global 75th quantile of fundamental frequency distribution")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return z3

    def total(self):
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=np.array(z2)
            z4=np.array(z3)[np.newaxis]
            z5=z4.T
            dataset=pd.DataFrame({"number_ of_syllables":z5[0,:],"number_of_pauses":z5[1,:],"rate_of_speech":z5[2,:],"articulation_rate":z5[3,:],"speaking_duration":z5[4,:],
                            "original_duration":z5[5,:],"balance":z5[6,:],"f0_mean":z5[7,:],"f0_std":z5[8,:],"f0_median":z5[9,:],"f0_min":z5[10,:],"f0_max":z5[11,:],
                            "f0_quantile25":z5[12,:],"f0_quan75":z5[13,:]})
            print (dataset.T)
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return;

    def pronunciation_posteriori_probability_score_percentage(self):
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=int(z2[13]) # will be the integer number 10
            z4=float(z2[14]) # will be the floating point number 8.3
            db= binom.rvs(n=10,p=z4,size=10000)
            a=np.array(db)
            b=np.mean(a)*100/10
            print ("Pronunciation_posteriori_probability_score_percentage= :%.2f" % (b))
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")
        return;

    def gender_mode_of_speech(self):
        try:
            print (self.objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
            z1=str( self.objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
            z2=z1.strip().split()
            z3=float(z2[8]) # will be the integer number 10
            z4=float(z2[7]) # will be the floating point number 8.3
            if z4<=114:
                g=101
                j=3.4
            elif z4>114 and z4<=135:
                g=128
                j=4.35
            elif z4>135 and z4<=163:
                g=142
                j=4.85
            elif z4>163 and z4<=197:
                g=182
                j=2.7
            elif z4>197 and z4<=226:
                g=213
                j=4.5
            elif z4>226:
                g=239
                j=5.3
            else:
                print("Voice not recognized")
                raise ValueError("Voice not recognized")
            def teset(a,b,c,d):
                d1=np.random.wald(a, 1, 1000)
                d2=np.random.wald(b,1,1000)
                d3=ks_2samp(d1, d2)
                c1=np.random.normal(a,c,1000)
                c2=np.random.normal(b,d,1000)
                c3=ttest_ind(c1,c2)
                y=([d3[0],d3[1],abs(c3[0]),c3[1]])
                return y
            nn=0
            mm=teset(g,j,z4,z3)
            while (mm[3]>0.05 and mm[0]>0.04 or nn<5):
                mm=teset(g,j,z4,z3)
                nn=nn+1
            nnn=nn
            if mm[3]<=0.09:
                mmm=mm[3]
            else:
                mmm=0.35
            if z4>97 and z4<=114:
                print("a Male, mood of speech: Showing no emotion, normal, p-value/sample size= :%.2f" % (mmm), (nnn))
            elif z4>114 and z4<=135:
                print("a Male, mood of speech: Reading, p-value/sample size= :%.2f" % (mmm), (nnn))
            elif z4>135 and z4<=163:
                print("a Male, mood of speech: speaking passionately, p-value/sample size= :%.2f" % (mmm), (nnn))
            elif z4>163 and z4<=197:
                print("a female, mood of speech: Showing no emotion, normal, p-value/sample size= :%.2f" % (mmm), (nnn))
            elif z4>197 and z4<=226:
                print("a female, mood of speech: Reading, p-value/sample size= :%.2f" % (mmm), (nnn))
            elif z4>226 and z4<=245:
                print("a female, mood of speech: speaking passionately, p-value/sample size= :%.2f" % (mmm), (nnn))
            else:
                print("Voice not recognized")
        except Exception as e:
            print(e)
            print ("Try again the sound of the audio was not clear")

    def get_function_list(self):
        # Get all attributes (including methods) of the class
        all_attributes = dict(inspect.getmembers(self))

        # Extract only the methods from the attributes
        function_list = [value.__name__ for key, value in all_attributes.items() if callable(value) and hasattr(value, '__call__') and isinstance(value, types.MethodType)]

        return function_list