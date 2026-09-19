#모듈 전체 import
import utils

print(utils.to_float("3.7"))
print(utils.VOLTAGE_HIGH)


#필요한 함수 또는 변수만 import
from utils import to_float, VOLTAGE_HIGH
print (to_float("3.7")) # utils. 호출 없이 사용


#이름 바꾸기
import utils as u
print(u.to_float("3.7"))