```markdown
# piecraft

![Example Chart](chart.png)

Minecraft 스타일의 픽셀/블록 감성 파이 차트 생성기입니다. 파이 자체의 모양(픽셀화, 3D 깊이, 색상/그라데이션)은 Minecraft 원본과 최대한 비슷하게 재현하며, 밑의 레이블(글씨)은 사용자 환경의 폰트를 사용합니다. (원하시면 동일한 폰트를 넣어 드립니다.)

설치 (개발 환경)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

간단 사용 예
```python
from piecraft import Pie

pie = Pie(200, title="Resources")
pie.add(40, "#FF6B6B", "Red")
pie.add(35, "#4D96FF", "Blue")
pie.add(25, "#6BCB77", "Green")
pie.save("chart.png")  # chart.png가 생성됩니다
```

설정 옵션 (Pie 생성자 / save)
- Pie(radius, title=None, pixel_scale=8)
  - radius: 파이 반지름(픽셀)
  - pixel_scale: 파이 픽셀화의 배율(값이 클수록 블록이 큼) — 기본 8
- save(path, font_path=None, font_size=14, bg=(30,30,30,255))
  - font_path: 특정 TTF 경로를 넣으면 레이블에 그 폰트를 사용합니다.
  - font_size: 레이블 폰트 크기

특징
- 픽셀화된(블록) 파이 아트: 작은 해상도로 렌더한 뒤 nearest-neighbor로 확대하여 블록 픽셀감을 만듭니다.
- 3D 깊이 효과: 여러 depth 레이어를 그려 입체감을 재현합니다.
- 색상 파싱(HEX 및 튜플 허용), 클램핑, 총합 0 처리(명확한 오류) 등 안전성 보강
- MIT 라이선스

테스트
- pytest 사용(간단한 이미지 생성/존재 확인)

기여
- PR/이슈 환영합니다. 간단한 기능 추가(색상 팔레트, 텍스트 레이아웃 개선, PNG 외 포맷) 제안해주세요.

라이선스
- MIT License (자세한 내용은 LICENSE 파일 참조)
```