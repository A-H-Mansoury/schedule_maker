class custom_data:
  
  WEEKDAYS = ['شنبه', 'يك شنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنج شنبه']

  def __init__(self, type, *args, **kwargs):
    self.type = type
    getattr(self, '__init_type_%d__'%(type//4))(*args, **kwargs)
  
  @staticmethod
  def time_overlap(a, b):
    overlap =  max(0, min(a.end_timestamp, b.end_timestamp) - max(a.start_timestamp, b.start_timestamp))
    return overlap > 0

  def __time2timestamp(self, string):
    hour, minute = string.split(':')
    return  60*int(hour) + int(minute) 

  def __init_type_0__(
    self,
    day: str,
    start_time: str,
    end_time: str,
    place: str = None
  ):

    self.day = self.WEEKDAYS.index(day)
    self.start_time = start_time
    self.end_time = end_time
    self.start_timestamp =  60*24*self.day + self.__time2timestamp(start_time)
    self.end_timestamp = 60*24*self.day + self.__time2timestamp(end_time)

  def __init_type_1__(
    self,
    date: str,
    start_time: str,
    end_time: str,
  ):
    self.date = date
    self.start_time = start_time
    self.end_time = end_time
    _, month, day = date.split('.')
    self.start_timestamp = 60*24*10 + 60*24*31*int(month) + 60*24*int(day) + self.__time2timestamp(start_time)
    self.end_timestamp = + 60*24*10 + 60*24*31*int(month) + 60*24*int(day) + self.__time2timestamp(end_time)
