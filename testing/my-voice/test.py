# Import the library dynamically
# mysp=__import__("my-voice-analysis") 

import service.myVoiceAnalysis as mysp
import pandas as pd
from praatio.textgrid import openTextgrid
from praatio.data_classes import point_tier, interval_tier
import os


file_path='audio/5.wav' # Audio File title
path= os.path.split(file_path)
print(path)

obj = mysp.MyVoiceAnalysis('audio/5.wav')
textgrid_file = "audio/5.TextGrid"
tg = openTextgrid(textgrid_file, includeEmptyIntervals=True)
# Extract tier information
tier_names = tg.tierNames
print(tier_names)

# Create empty DataFrames for PointTiers and IntervalTiers
point_tier_df = pd.DataFrame()
interval_tier_df = pd.DataFrame()

# Iterate through each tier in the TextGrid
for tier_name in tier_names:
    tier = tg._tierDict[tier_name]

    # Extract information from PointTier or IntervalTier
    if isinstance(tier, point_tier.PointTier):
        pointer_name = tier_name
        tier_data = [(point[0], point[1]) for point in tier.entries]
        tier_df = pd.DataFrame(tier_data, columns=["number", "mark"])
        
        # Concatenate with the PointTier DataFrame
        point_tier_df = pd.concat([point_tier_df, tier_df], axis=1)

    elif isinstance(tier, interval_tier.IntervalTier):
        interval_name = tier_name
        tier_data = [(interval[0], interval[1], interval[2]) for interval in tier.entries]
        tier_df = pd.DataFrame(tier_data, columns=["xmin", "xmax", "text"])
        
        # Concatenate with the IntervalTier DataFrame
        interval_tier_df = pd.concat([interval_tier_df, tier_df], axis=1)

# Sort DataFrames by 'xmin'
point_tier_df = point_tier_df.sort_values(by='number').reset_index(drop=True)
interval_tier_df = interval_tier_df.sort_values(by='xmin').reset_index(drop=True)

# Display the DataFrames
print("PointTier DataFrame:")
print(point_tier_df)

print("\nIntervalTier DataFrame:")
print(interval_tier_df)



# obj.total()#mysp.mysptotal(p,c)
# obj.gender_mode_of_speech()#mysp.myspgend(p,c)
# obj.number_of_syllables()#mysp.myspsyl(p,c)
# obj.number_of_pauses()#mysp.mysppaus(p,c)
# obj.rate_of_speech()#mysp.myspsr(p,c)
# obj.articulation_rate()#mysp.myspatc(p,c)
# obj.speaking_duration()#mysp.myspst(p,c)
# obj.original_duration()#mysp.myspod(p,c)
# obj.balance()#mysp.myspbala(p,c)
# obj.myspf0mean()#mysp.myspf0mean(p,c)
# obj.myspf0sd()#mysp.myspf0sd(p,c)
# obj.myspf0med()#mysp.myspf0med(p,c)
# obj.myspf0min()#mysp.myspf0min(p,c)
# obj.myspf0max()#mysp.myspf0max(p,c)
# obj.myspf0q25()#mysp.myspf0q25(p,c)
# obj.myspf0q75()#mysp.myspf0q75(p,c)
# obj.pronunciation_posteriori_probability_score_percentage()#mysp.mysppron(p,c)












