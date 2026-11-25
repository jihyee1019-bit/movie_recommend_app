
import streamlit as st

# =====================================
# 1. 영화 데이터 리스트
# =====================================

movies = [
    {"title": "다크 나이트", "genres": ["스릴러", "드라마"], "stories": ["복수", "성장"]},
    {"title": "존 윅", "genres": ["스릴러"], "stories": ["복수", "생존"]},
    {"title": "기생충", "genres": ["스릴러", "드라마", "코미디"], "stories": ["가족", "생존"]},
    {"title": "나이브스 아웃", "genres": ["스릴러", "코미디"], "stories": ["가족"]},
    {"title": "라라랜드", "genres": ["로맨스", "드라마"], "stories": ["사랑", "성장"]},
    {"title": "어바웃 타임", "genres": ["로맨스", "코미디", "판타지", "드라마"], "stories": ["사랑", "가족", "성장"]},
    {"title": "이터널 선샤인", "genres": ["로맨스", "SF", "드라마"], "stories": ["사랑"]},
    {"title": "트루먼 쇼", "genres": ["드라마", "코미디", "SF"], "stories": ["성장", "생존"]},
    {"title": "인터스텔라", "genres": ["SF", "드라마"], "stories": ["생존", "가족", "사랑"]},
    {"title": "매트릭스", "genres": ["SF", "스릴러"], "stories": ["생존", "성장"]},
    {"title": "아바타", "genres": ["SF", "판타지"], "stories": ["성장", "사랑", "생존"]},
    {"title": "반지의 제왕: 반지 원정대", "genres": ["판타지"], "stories": ["우정", "생존", "성장"]},
    {"title": "겟 아웃", "genres": ["스릴러"], "stories": ["생존"]},
    {"title": "샤이닝", "genres": ["스릴러"], "stories": ["가족"]},
    {"title": "셔터 아일랜드", "genres": ["스릴러", "드라마"], "stories": ["복수"]},
    {"title": "센과 치히로의 행방불명", "genres": ["애니메이션", "판타지"], "stories": ["성장", "우정"]},
    {"title": "인사이드 아웃", "genres": ["애니메이션", "코미디"], "stories": ["성장", "가족"]},
    {"title": "코코", "genres": ["애니메이션", "판타지"], "stories": ["가족", "성장"]},
    {"title": "너의 이름은.", "genres": ["애니메이션", "로맨스", "판타지"], "stories": ["사랑", "성장"]},
    {"title": "월-E", "genres": ["애니메이션", "SF", "로맨스"], "stories": ["사랑", "생존"]}
]


# =====================================
# 2. 사용자 취향과 영화 일치도 분석 함수
# =====================================

def analyze_movie(movie, selected_genre, selected_story):

    match_score = 0

    # 장르가 일치하면 1점 추가
    if selected_genre in movie["genres"]:
        match_score += 1

    # 스토리 요소가 일치하면 1점 추가
    if selected_story in movie["stories"]:
        match_score += 1

    return match_score


# =====================================
# 3. 영화 추천 함수
# =====================================

def recommend_movies(selected_genre, selected_story):

    movie_scores = []

    # for문으로 20개 영화의 정보를 하나씩 확인
    for movie in movies:

        score = analyze_movie(
            movie,
            selected_genre,
            selected_story
        )

        # 영화 정보와 일치도 점수를 리스트에 저장
        movie_scores.append({
            "title": movie["title"],
            "genres": movie["genres"],
            "stories": movie["stories"],
            "score": score
        })

    # 일치도 점수가 높은 순서대로 정렬
    movie_scores.sort(
        key=lambda movie: movie["score"],
        reverse=True
    )

    # 상위 3개 영화 반환
    return movie_scores[:3]


# =====================================
# 4. 앱 화면 구성
# =====================================

st.set_page_config(
    page_title="맞춤 영화 추천",
    page_icon="🎬",
    layout="centered"
)

st.title("맞춤 영화 추천")
st.write("나의 취향을 선택하고 영화를 추천받아 보세요!")

st.divider()

# (1) 선호하는 장르 선택
st.subheader("(1) 선호하는 장르 선택")

genre_list = [
    "스릴러", "드라마", "애니메이션",
    "코미디", "로맨스", "판타지", "SF"
]

selected_genre = st.radio(
    "원하는 장르 하나를 선택해 주세요.",
    genre_list,
    index=None
)

st.divider()

# (2) 선호하는 스토리 선택
st.subheader("(2) 선호하는 스토리 선택")

story_list = [
    "복수", "성장", "생존",
    "사랑", "우정", "가족"
]

selected_story = st.radio(
    "좋아하는 스토리 요소 하나를 선택해 주세요.",
    story_list,
    index=None
)

st.divider()


# =====================================
# 5. 추천받기 버튼 및 결과 화면
# =====================================

# 두 가지 취향을 모두 선택했을 때 버튼 표시
if selected_genre and selected_story:

    if st.button("✨ 추천받기", use_container_width=True):

        # 영화 추천 함수 실행
        top_movies = recommend_movies(
            selected_genre,
            selected_story
        )

        st.divider()

        st.success("취향에 맞는 영화를 찾았습니다!")

        st.subheader("나의 맞춤 영화 TOP 3")

        # 결과를 표 형태로 출력
        result_data = []

        for index, movie in enumerate(top_movies):

            if movie["score"] == 2:
                reason = "장르와 스토리 모두 일치"
            elif movie["score"] == 1:
                reason = "장르 또는 스토리 일치"
            else:
                reason = "일치 항목 없음"

            result_data.append({
                "순위": f"{index + 1}위",
                "영화 제목": movie["title"],
                "장르": ", ".join(movie["genres"]),
                "스토리 요소": ", ".join(movie["stories"]),
                "추천 점수": f"{movie['score']}/2",
                "추천 이유": reason
            })

        st.table(result_data)

else:
    st.info(
        "장르와 스토리를 모두 선택하면 "
        "추천받기 버튼이 나타납니다."
    )
