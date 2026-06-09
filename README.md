# set_ref

Nuke 툴 — 선택한 **CornerPin2D / Transform** 노드를 **현재 프레임 기준 reference pose**로 베이크한다.

- **CornerPin2D**: 현재 프레임의 `to` 값을 `from` 에 구워 넣어 그 프레임을 매치 기준으로 고정.
- **Transform**: 현재 프레임이 중립 포즈가 되도록 키값을 in-place 정규화.
- 노드 `label` 에 `ref: <frame>` 표기. 여러 노드 동시 선택 가능, Undo 한 번에 묶임.

## 설치 (menu.py)

1. `JM_set_ref.py` 를 `~/.nuke/python/` 에 복사.
2. `~/.nuke/menu.py` 에 추가:

```python
import nuke
import JM_set_ref

_menu = nuke.menu("Nuke").addMenu("JM Tools")
_menu.addCommand("Set Ref (CornerPin / Transform)", "JM_set_ref.set_ref()", "shift+c")
```

> Shift+C 가 겹치면 마지막 인자만 바꾸면 된다 (예: `"ctrl+shift+c"`).

## 사용

CornerPin2D / Transform 노드 선택 → 기준 프레임으로 이동 → **Shift+C**.
