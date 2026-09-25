"""도시생활 적합도 테스트."""

# 딕셔너리: 유형 이름을 키로 사용하여 설명과 색상 등의 정보를 보관합니다.
CITY_TYPES = {
    "green": {
        "name": "녹지친화형", "english": "GREEN EXPLORER", "symbol": "01",
        "color": "#426a4e", "background": "#e3ecd8",
        "title": "나의 일상에는,\n초록 한 조각이 필요해요.",
        "description": "가까운 공원과 걷기 좋은 길에서 에너지를 얻는 당신. 멀리 떠나지 않아도 계절의 변화를 만날 수 있는 동네가 잘 어울려요.",
        "short": "산책길에서 발견하는 일상의 여유",
        "tags": ["공원 접근성", "나무 그늘", "산책로"],
        "tip": "관심 있는 동네에서 공원까지 직접 걸어보세요. 거리뿐 아니라 그늘과 횡단보도, 길의 연결도 함께 살펴보면 좋아요.",
    },
    "transit": {
        "name": "대중교통형", "english": "CONNECTED MOVER", "symbol": "02",
        "color": "#416785", "background": "#dde9f0",
        "title": "가볍게 나서면,\n도시 어디든 가까이.",
        "description": "차 없이도 자유롭게 이동하는 일상을 좋아하는 당신. 버스와 지하철이 잘 연결되고 정류장까지 걷기 편한 동네가 잘 어울려요.",
        "short": "어디로든 가볍게 연결되는 일상",
        "tags": ["역세권", "환승 편의", "보행 연결"],
        "tip": "평소 이동하는 시간대에 경로를 확인해보세요. 역까지의 거리와 함께 배차 간격, 환승 횟수도 비교하면 좋아요.",
    },
    "active": {
        "name": "도심활동형", "english": "CITY ENTHUSIAST", "symbol": "03",
        "color": "#aa6549", "background": "#f3e2d7",
        "title": "문밖을 나서면,\n새로운 하루가 시작돼요.",
        "description": "다양한 가게와 맛집, 활기 있는 거리에서 즐거움을 찾는 당신. 필요한 것을 가까이에서 해결하고 새로운 장소를 발견하는 동네가 잘 어울려요.",
        "short": "골목마다 새로운 즐거움이 있는 곳",
        "tags": ["생활 편의", "카페와 맛집", "활기 있는 거리"],
        "tip": "자주 이용하는 가게가 도보 생활권에 있는지 살펴보세요. 평일과 주말에 각각 방문하면 거리의 분위기를 더 잘 알 수 있어요.",
    },
    "quiet": {
        "name": "조용한주거형", "english": "SLOW NEIGHBOR", "symbol": "04",
        "color": "#857244", "background": "#efe9d6",
        "title": "하루의 끝에는,\n고요한 쉼이 기다려요.",
        "description": "분주한 하루 뒤 편안하게 쉴 수 있는 공간을 아끼는 당신. 차분한 골목과 안정적인 생활 리듬이 있는 동네가 잘 어울려요.",
        "short": "나만의 속도로 편안하게 쉬는 동네",
        "tags": ["차분한 골목", "휴식", "주거환경"],
        "tip": "낮과 저녁에 동네를 걸으며 주변 소리를 들어보세요. 큰 도로와 상업시설의 위치, 집으로 가는 길의 조명도 살펴보면 좋아요.",
    },
    "culture": {
        "name": "문화생활형", "english": "CULTURE SEEKER", "symbol": "05",
        "color": "#80678c", "background": "#ebe2ee",
        "title": "익숙한 일상에도,\n새로운 영감이 필요해요.",
        "description": "전시와 공연, 책을 통해 일상을 풍성하게 만드는 당신. 다양한 문화 공간을 가깝게 만날 수 있는 동네가 잘 어울려요.",
        "short": "취향과 영감이 쌓이는 하루",
        "tags": ["전시와 공연", "도서관", "동네 책방"],
        "tip": "문화시설의 개수뿐 아니라 실제 프로그램과 운영 시간을 찾아보세요. 자주 가고 싶은 공간인지가 더 중요해요.",
    },
}

# 리스트 안의 딕셔너리: 각 유형에 두 문항씩 배정하여 최고 점수를 같게 맞춥니다.
QUESTIONS = [
    {"id": 1, "type": "green", "text": "집 가까이에 걸어서 갈 수 있는\n공원이나 산책로가 있으면 좋겠어요.", "hint": "잠깐의 산책도 일상의 중요한 부분인가요?"},
    {"id": 2, "type": "transit", "text": "자동차 없이도 대중교통으로\n편하게 이동할 수 있으면 좋겠어요.", "hint": "내가 원하는 이동 방식을 떠올려보세요."},
    {"id": 3, "type": "active", "text": "카페와 식당, 다양한 가게가\n집 근처에 모여 있으면 좋겠어요.", "hint": "생활 속 선택지가 가까이 있는 것을 좋아하나요?"},
    {"id": 4, "type": "quiet", "text": "집 주변에서는 번화함보다\n조용하고 차분한 분위기가 좋아요.", "hint": "집으로 돌아오는 길의 풍경을 상상해보세요."},
    {"id": 5, "type": "culture", "text": "전시나 공연을 보러\n부담 없이 자주 갈 수 있으면 좋겠어요.", "hint": "문화생활이 내 일상에서 차지하는 자리는 어느 정도인가요?"},
    {"id": 6, "type": "green", "text": "나무와 녹지가 있는 길에서\n계절의 변화를 느끼는 게 좋아요.", "hint": "매일 만나는 자연이 내게 얼마나 중요한가요?"},
    {"id": 7, "type": "transit", "text": "집을 고를 때 역이나 정류장까지의\n거리와 교통 연결을 중요하게 생각해요.", "hint": "출퇴근뿐 아니라 평소 이동도 함께 생각해보세요."},
    {"id": 8, "type": "active", "text": "새로운 가게를 발견하고\n활기 있는 거리를 구경하는 게 좋아요.", "hint": "여유 시간이 생겼을 때 가고 싶은 장소를 떠올려보세요."},
    {"id": 9, "type": "quiet", "text": "동네에서는 북적이는 활동보다\n느긋하게 쉬는 시간을 보내고 싶어요.", "hint": "가장 편안하다고 느끼는 주말은 어떤 모습인가요?"},
    {"id": 10, "type": "culture", "text": "도서관이나 동네 책방처럼\n취향을 넓힐 공간이 가까우면 좋겠어요.", "hint": "새로운 이야기를 만날 수 있는 공간을 생각해보세요."},
]

CHOICES = [
    {"value": 5, "label": "매우 그렇다"},
    {"value": 4, "label": "그렇다"},
    {"value": 3, "label": "보통이다"},
    {"value": 2, "label": "그렇지 않다"},
    {"value": 1, "label": "전혀 그렇지 않다"},
]


def check_answer(answer):
    """함수 + 조건문: 1~5의 정수만 유효한 응답으로 인정합니다."""
    if type(answer) is int and 1 <= answer <= 5:
        return True
    else:
        return False


def answer_to_points(answer):
    """if / elif / else를 사용하여 답변을 0~4점으로 변환합니다."""
    if not check_answer(answer):
        raise ValueError("답변은 1~5 사이의 정수여야 합니다.")
    if answer == 5:
        return 4
    elif answer == 4:
        return 3
    elif answer == 3:
        return 2
    elif answer == 2:
        return 1
    else:
        return 0


def find_best_types(scores):
    """반복문 + 조건문: 가장 높은 점수를 찾고, 동점 유형도 모두 보관합니다."""
    best_score = -1
    best_types = []
    for city_type, score in scores.items():
        if score > best_score:
            best_score = score
            best_types = [city_type]
        elif score == best_score:
            best_types.append(city_type)
    return best_types


def calculate_result(answers):
    """각 요청마다 새 점수표를 만들어 다른 사용자의 응답과 섞이지 않게 합니다."""
    if not isinstance(answers, list) or len(answers) != len(QUESTIONS):
        raise ValueError("10개의 질문에 모두 답해주세요.")

    scores = {}
    maximums = {}
    for city_type in CITY_TYPES:
        scores[city_type] = 0
        maximums[city_type] = 0

    # for 반복문: 질문과 사용자 응답을 하나씩 확인하여 유형별로 점수를 더합니다.
    for index in range(len(QUESTIONS)):
        answer = answers[index]
        city_type = QUESTIONS[index]["type"]
        scores[city_type] += answer_to_points(answer)
        maximums[city_type] += 4

    best_types = find_best_types(scores)
    percentages = {}
    for city_type, score in scores.items():
        percentages[city_type] = round(score / maximums[city_type] * 100)

    if max(scores.values()) == 0:
        mode = "exploring"
        best_types = []
    elif len(best_types) > 1:
        mode = "mixed"
    else:
        mode = "single"

    return {"scores": scores, "maximums": maximums, "percentages": percentages,
            "best_types": best_types, "mode": mode}
