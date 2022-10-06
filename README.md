# instargram_clonecoding_project

생성일: 2022년 9월 29일 오후 5:21

# **B3 팀**

- 팀명 : 비상 ( 높게오르자는 의미와 .. 현재 실력이 '비상'이라는 뜻도 있습니다.)
- 팀장 : 현준호
- 팀원 : 강기훈, 김경민, 김민수, 이원채
- 프로젝트 역할
    - 강기훈
        - 회원가입, 로그인, post, 개인프로필 기능 구현
    - 김경민
        - 스토리 , 팔로우,팔로윙 기능 구현
    - 김민수
        - 좋아요 ,댓글 ,회원가입, 로그인, post 기능 구현
    - 이원채
        - 좋아요 ,댓글 ,회원가입, 로그인, post 기능 구현
    - 현준호
        - 포스트 - 모달창을 띄우기, 북마크, 프로필 창 기능 구현
    

## Wireframe
![Untitled](https://user-images.githubusercontent.com/113074274/194221236-aebee738-31da-4d3e-a7c6-0671e87cd0cb.png)
![Untitled 1](https://user-images.githubusercontent.com/113074274/194221275-7de0b1ee-693c-4e01-b19a-d2ea0739140a.png)
![Untitled 2](https://user-images.githubusercontent.com/113074274/194221279-05c17e4a-bc07-4d8b-a2a1-17a93768c410.png)
![Untitled 3](https://user-images.githubusercontent.com/113074274/194221280-11419b16-53ae-4e18-a8b3-9c52f39ee51c.png)
![Untitled 4](https://user-images.githubusercontent.com/113074274/194221281-bc9fd7a2-f072-47b3-9862-4fa7cae7797f.png)
![Untitled 5](https://user-images.githubusercontent.com/113074274/194221285-2b206874-4358-4f63-9cb7-82a9ef01c5dd.png)
![Untitled 6](https://user-images.githubusercontent.com/113074274/194221289-9e070ac6-be78-460d-8ce6-e766f29afd05.png)
![Untitled 7](https://user-images.githubusercontent.com/113074274/194221291-e5656ef4-6ef0-4056-8442-ee03804bd66a.png)


## ERD
![Untitled 8](https://user-images.githubusercontent.com/113074274/194221303-5e837459-f2a0-4367-8af7-7789033b6cb7.png)


## 변경 ERD
![%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_2022-10-05_%EC%98%A4%ED%9B%84_9 25 18](https://user-images.githubusercontent.com/113074274/194221326-e83d7326-7ca0-4744-b75f-6a5988706245.png)

## API

- 회원가입, 로그인, 로그아웃
- 정보 수정, 비밀번호 변경
- 개인프로필
- 친구 추천
- 팔&언팔
- 게시물 생성, 수정, 삭제, 좋아요
- 스토리 생성, 보기
- 댓글 생성, 삭제 (대댓글 생성, 삭제)
- 카카오 로그인

| 기능 | method | url | request | response | 비고 |
| --- | --- | --- | --- | --- | --- |
| 회원가입 | GET | /user/join |  | join.html |  |
|  | POST | /user/join |  | login.html |  |
| 로그인 | GET | /user/login |  | login.html |  |
|  | POST | /user/login |  | index.html |  |
| 로그아웃 | GET | /user/logout |  | login.html |  |
|  |  |  |  |  |  |
| 정보수정 | GET | /user/update |  | user/update.html |  |
| 정보수정 | POST | /user/update |  |  |  |
| 비밀번호변경 | GET | /user/change_password |  |  |  |
|  | POST | /user/change_password |  |  |  |
| 프로필 | GET | /<str:nickname> |  | profile.html |  |
| 친구 추천 | GET | /<str:nickname>/recommand |  | recommand.html |  |
|  |  |  |  |  |  |
| 팔&언팔 | GET | /follow/<int:user_id> |  |  |  |
|  |  |  |  |  |  |
| 게시물생성 | POST | /post |  |  |  |
| 게시글수정 | POST | /post/update/<int:post_id> |  |  |  |
| 게시글 상세 | GET | /detail/<int:post_id> |  | / |  |
| 게시글 삭제 | GET | /delete/<int:post_id> |  | / |  |
| 게시글 좋아요 | GET | /like/<int:post_id> |  | / |  |
| 게시글 저장 | GET | /bookmark/<int:post_id> |  | index.html |  |
|  |  |  |  |  |  |
| 스토리 생성 | POST | /story/<str:nickname> |  |  |  |
| 스토리 보기 | GET | /story/create |  | story_view.html |  |
|  |  |  |  |  |  |
| 댓글생성 | POST | /comment/<int:post_id> |  | index.html |  |
| 댓글삭제 | GET | /comment/delete/<int:comment_id> |  | / |  |
|  |  |  |  |  |  |
| 카카오로그인 | GET | /account/login/kakao |  |  |  |
|  | GET | account/login/kakao/callback |  |  |  |
