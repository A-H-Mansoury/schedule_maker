import pandas as pd

path = ""
days = [': شنبه']
days.append(': يك شنبه')
days.append(': دو شنبه')
days.append(': سه شنبه')
days.append(': چهار شنبه')
days.append(': پنج شنبه')

def get_input_excel_path(pth):
    global path
    path = pth
    return run()

def day_encode(s):
  global days
  s = str(s)
  temp = []
  for j in range(6):
     if s.find(days[j]) > -1:
       temp.append(j)
  return str(temp)

def run():
  df = pd.read_excel(path)
  
  a = df['زمان و مكان ارائه/ امتحان']
  a = pd.DataFrame(map(lambda x : str(x)[str(x).find('-')-5:6+str(x).find('-')], a))
  res  = pd.DataFrame(list(map(lambda x : str(x).split('-'), a[0])), columns=['Start_time','end_time'])
  res['id'] = list(map(lambda x : str(x), df['شماره و گروه درس']))
  res['days'] = pd.DataFrame(map(day_encode, df['زمان و مكان ارائه/ امتحان']))
  res['prof']  = pd.DataFrame(map(lambda x : x.replace('<BR>', '#'),df['نام استاد']))
  res['course_name'] = df['نام درس']

  return res