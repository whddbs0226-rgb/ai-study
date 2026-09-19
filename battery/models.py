from pydantic.main import BaseModel
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
        return [cell for cell in self.cells if cell.is_abnormal()]

    def summary(self):
        # "MOD-01: 셀 3개, 이상 1개, 평균 3.72V" 형태 문자열 반환
        total_cells = len(self.cells)
        abnormal_count = len(self.abnormal_cells())
        avg_v = self.avg_voltage()
        return f"{self.component_id}: 셀 {total_cells}개, 이상 {abnormal_count}개, 평균 {avg_v:.2f}V"


# battery/models.py
class CellRow(BaseModel):
    timestamp: str
    cell_id: str
    voltage: float
    current: float
    temp: float