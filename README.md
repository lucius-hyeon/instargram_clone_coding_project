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

![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled.png)

![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%201.png)


![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%202.png%0D) 
![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%203.png%0D) 
![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%204.png%0D) 
![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%205.png%0D) 
![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%206.png%0D) 







## ERD
![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%207.png%0D) 


## 변경 ERD
![Untitled](c:/Users/Lucius/Downloads/Export-12e9096e-9b21-4a9d-a3f1-5dd1a52101b7/instargram_clonecoding_project%2011277d938d6145a2a278d17b24289545/Untitled%208.png) 

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
https://www.youtube.com/watch?v=8IxAmlwLtdM