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

![Untitled](https://user-images.githubusercontent.com/113074274/194245538-9fd62268-52b9-4ada-b6f2-57b54f716fbd.png)
![Untitled 1](https://user-images.githubusercontent.com/113074274/194245552-154c69ac-4e4d-4d01-9bd6-925905edc75e.png)
![Untitled 2](https://user-images.githubusercontent.com/113074274/194245556-4eff6d60-5d52-4b17-9393-c17264874d4b.png)
![Untitled 3](https://user-images.githubusercontent.com/113074274/194245564-0cc9e084-4d0a-4beb-ace3-5c7b9a25e6da.png)
![Untitled 4](https://user-images.githubusercontent.com/113074274/194245565-7ac7aed5-a2ad-48c2-bf21-8f0c17a8e092.png)
![Untitled 5](https://user-images.githubusercontent.com/113074274/194245569-e61ae39f-e083-4494-aca9-8ac118a89af6.png)
![Untitled 6](https://user-images.githubusercontent.com/113074274/194245572-3fa2de1e-d8f5-4d81-8f6c-6c339d98ec06.png)
![Untitled 7](https://user-images.githubusercontent.com/113074274/194245573-717be0a4-13bf-4799-b658-e7659f7c9e6d.png)




## ERD
![Untitled 8](https://user-images.githubusercontent.com/113074274/194245587-4966576b-2640-406c-af4c-e1e9e3167ca5.png)

## 변경 ERD
![%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_2022-10-05_%EC%98%A4%ED%9B%84_9 25 18](https://user-images.githubusercontent.com/113074274/194245622-56334ab0-2f8a-4b52-93f6-bbeeafaeb820.png)


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

## 시연영상
[![미리보기](https://img.youtube.com/vi/8IxAmlwLtdM/0.jpg)](https://www.youtube.com/watch?v=8IxAmlwLtdM)
