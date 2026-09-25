
from functools import lru_cache # 같은 인자로 부르면 이전 결과를 재사용
from fastapi import Depends # @Autowired와 같은 사용
from typing import Annotated
from battery.config import Settings

@lru_cache
def get_settings() -> Settings:
    return Settings()      # 한 번만 만들고 재사용


SettingsDep = Annotated[Settings, Depends(get_settings)]