import pandas as pd
from  models import Place,PlaceOption
 
df = pd.read_csv('user.csv')
 
for _, row in df.iterrows():
    dict_data = row.to_dict()
    Place.objects.create(**dict_data)
 
question = Place.objects.all()
print(question.count()) # 5