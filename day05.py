#클래스와 __init__
from day03 import high
class BatteryCell:
    def __init__(self, cell_id, voltage, temp):
        self.cell_id = cell_id
        self.voltage = voltage
        self.temp = temp

    
    def is_abnormal(self, high=4.0, low=3.0):
        return not (low <= self.voltage <= high)

    def report(self):
        status = "이상" if self.is_abnormal() else "정상"
        return f"{self.cell_id}: {self.voltage}V ({status})"

c1 = BatteryCell("CELL-001", 3.7, 28.4) # __init__을 통해 self에 값 저장
c2 = BatteryCell("CELL-002", 4.2, 31.0)

print(c1.report())
print(c2.report())
print(c2.is_abnormal())


#상속
class Component:
    def __init__(self, component_id):
        self.component_id = component_id

    def describe(self):
        return f"부품 {self.component_id}"


class BatteryModule(Component):
    def __init__(self, component_id, cells):
        super().__init__(component_id)
        self.cells = cells

    def describe(self):
        return f"모듈 {self.component_id} (셀 {len(self.cells)}개)"

    def avg_voltage(self):
        return sum(c.voltage for c in self.cells) / len(self.cells)

    def abnormal_cells(self):
        # 이상 셀 객체 리스트 반환 (컴프리헨션 사용)
        pass

    def summary(self):
        # "MOD-01: 셀 3개, 이상 1개, 평균 3.72V" 형태 문자열 반환
        pass


m = BatteryModule("MOD-01", [c1, c2])
print(m.describe())
print(f"{m.avg_voltage():.3f}V")
print(isinstance(m, Component))


#__str__ 과 __repr__ (던더메서드)
class BatteryCell:
    def __init__(self, cell_id, voltage):
        self.cell_id = cell_id
        self.voltage = voltage

    def __str__(self):  # string 출력 ( print(c), str(c) 에서 자동 실행)
        return f"{self.cell_id} ({self.voltage}V)"

    def __repr__(self): # 개발자기 보기위한 출력 ( print([c, c] 에서 자동 실행))
        return f"BatteryCell({self.cell_id!r}, {self.voltage})"


c = BatteryCell("CELL-001", 3.7)
print(c)
print([c, c])



# 실습
