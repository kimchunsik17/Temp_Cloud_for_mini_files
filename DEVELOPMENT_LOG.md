개발 일지

프로젝트 개요

프로젝트명: 임시 파일 클라우드

개발 기간:  2025.10.23 ~ 2025.XX.XX

목표: 로그인이 필요없는 클라우드 서비스

개발 과정

Week 1 (예: 10/20 ~ 10/26)

Day 1 (예: 10/23)

프로젝트 기획

작업 내용:

요구사항 분석 및 GEMINI.md 작성

기술 스택 확정 (Django, Bootstrap)

Git 전략 수립 (main, develop, feat 브랜치)

사이트 뼈대 완성
파일을 업로드하고 파일 ID와 pw를 통해 다운로드할 수 있는 기능을 추가
admin 페이지와 접속 방법 추가
admin 페이지의 기능 추가(파일 삭제, ip 당 파일 크기, 업로드 가능한 개수 수정 기능)
페이지 별로 이동 가능한 버튼 추가

Gemini CLI 사용 프롬프트:

- **User:** `https://github.com/kimchunsik17/Temp_Cloud_for_mini_files 에 연결하고 branch 해줄래`
- **Agent:** `I can do that. I will initialize a git repository, add the remote origin, and create a new branch. What would you like to name the branch?`
- **User:** `main`
- **User:** `다시 해줘`
- **Agent:** `I have already connected to the repository and set up the main branch. Could you please clarify what you would like me to do again? Do you want to create a different branch, or something else?`
- **User:** `지금까지 만든 내용을 push 해줘`
- **User:** `GEMINI.md 파일을 기반으로 프로젝트를 시작해줘`
- **User:** `먼저 만들어진 내용을 테스트해보고 싶어`
- **User:** `지금까지의 내용을 branch해줄래`
- **Agent:** `I can create a new branch for you. What would you like to name the new branch?`
- **User:** `bone`
- **User:** `push`
- **User:** `bone을 main에 push해줘`
- **User:** `내가 한 명령어들 DEVEOPMENT_GEMINI_LOG.md 파일에 기록되고 있어?`
- **Agent:** `I have a memory that you wanted me to update DEVELOPMENT_LOG_2.md with the commands you entered. Could you please clarify: 1. Is the correct file name DEVEOPMENT_GEMINI_LOG.md or DEVELOPMENT_LOG_2.md? 2. Do you want me to record the commands I execute (my tool calls) or the commands you enter (your prompts to me)? Currently, I have not been recording my tool calls in any file. I can check the content of DEVEOPMENT_GEMINI_LOG.md if you'd like.`
- **User:** `응`
- **Agent:** `The DEVEOPMENT_GEMINI_LOG.md file is currently empty. To clarify, could you please tell me: 1. Is the correct file name DEVEOPMENT_GEMINI_LOG.md or DEVELOPMENT_LOG_2.md? 2. Do you want me to record the commands I execute (my tool calls) or the commands you enter (your prompts to me)?`
- **User:** `2번`
- **Agent:** `Okay, you want me to record the commands I execute (my tool calls). Now, regarding the file name, is it DEVEOPMENT_GEMINI_LOG.md or DEVELOPMENT_LOG_2.md that you want me to use for recording?`
- **User:** `전자야`
- **User:** `설정을 수정할게 내가 한 지시문들을 DEVELOPMENT_LOG.md 파일에 Gemini CLI 사용 프롬프트 부분에 차례로 넣어줘`
- **User:** `전자가 좋겠어`
- **User:** `내가 한 모든 프롬프트를 넣어줘`
- **User:** `후자야`
- **User:** `됐어? 그리고 내가 한 지시문에 대한 네 질문도 같이 넣어줬으면 해`
- **User:** `이제 작업을 계속하자 현재 페이지는 사용자가 업로드한 파일을 다운로드할 때 확장자가 아예 입력되지 않는 오류가 있어`
- **Agent:** `The merge operation was cancelled by you, so it didn't actually complete. Therefore, it didn't take any time to execute. If a merge operation were to take a long time, it would typically be due to complex conflicts between the branches being merged, requiring manual resolution. However, in this instance, the process was interrupted.`
- **User:** `어드민 페이지가 작동하는 걸 확인했어 이제 서버를 종료해admin 페이지에 기능을 추가해줘 지금까지 업로드된 모든 파일에 대한 정보를 볼 수 있도록 업로드한 사람의 ip 주소도 같이 보여져야 해`
- **Agent:** `I can create a new branch for you. What would you like to name it? Or do you want to switch to an existing branch, or something else?`
- **User:** `어드민 페이지에 접속할 때 사용할 파일을 준비해줘 비밀번호는 내게 알려주고`
- **Agent:** `Okay, I will postpone the merge. I will create a new branch for adding admin functionality. First, I'll switch to the main branch, then create a new branch named feat/admin-page from there. After that, I will implement the admin functionality, including a new view, URL, and template, and modify the upload view to handle access to the admin page based on a specific password.`
- **User:** `어드민 페이지에 접속하기 위한 파일은 특정 암호문으로 이루어진 파일이어야 해`
- **Agent:** `To access the admin page, you need to upload any file using the upload form and enter "1234" as the password. This will redirect you to the admin page.`
- **User:** `key파일을 admin 접속을 위한 파일로 만들어줘`
- **Agent:** `Okay, I understand. The admin page should be accessible only if the uploaded file contains a specific password phrase. I will modify the upload_view in cloud_storage/views.py to read the content of the uploaded file. If the content matches a predefined password phrase, it will redirect to the admin page; otherwise, it will proceed with the regular file upload process. First, I'll read the cloud_storage/views.py file.`
- **User:** `admin 페이지가 작동하는지 보고 싶어 서버를 실행해줘`
- **Agent:** `I have implemented the admin access functionality. To access the admin page, you need to upload a file whose content is exactly admin_access_granted. What would you like to do next?`
- **User:** `admin 페이지가 작동하는 걸 확인했어 이제 서버를 종료해admin 페이지에 기능을 추가해줘 지금까지 업로드된 모든 파일에 대한 정보를 볼 수 있도록 업로드한 사람의 ip 주소도 같이 보여져야 해`
- **Agent:** `I have prepared and committed the key file for admin access. What's next?`
- **User:** `현재 추가된 내용을 admin_fun 이라는 이름으로 branch 해줘`
- **Agent:** `The user wants to see if the admin page is working and wants me to start the server. I am currently on the feat/admin-page branch. I will start the Django development server. Command: python manage.py runserver I will inform the user that they can access the application in their browser after the server starts. They will need to upload the key file to access the admin page.`
- **User:** `push해줘`
- **Agent:** `Okay, the admin page is confirmed working. I will now add functionality to display all uploaded file information, including the uploader's IP address, on the admin page. This involves modifying the UploadedFile model to store IP addresses, updating the upload_view to capture this data, and then updating the admin_page_view and admin_page.html to display it. First, I'll read cloud_storage/models.py to add the ip_address field.`
- **User:** `지금까지 했던 지시문들을 다시 기록에 추가해줄래`
- **Agent:** `I have added the functionality to display uploaded file information, including IP addresses, on the admin page. What would you like to do next?`
- **Agent:** `I have created and switched to the admin_fun branch. What's next?`
- **Agent:** `The admin_fun branch has been successfully pushed to the remote repository.`

Day 2 (예: 10/21)

작업 내용:

(여기에 작업 내용 기록)

Gemini CLI 사용 프롬프트:

(여기에 Gemini CLI 명령어 기록)

Week 2 (날짜)

Day X (날짜)

작업 내용:

Gemini CLI 사용 프롬프트:

## 2025-10-23: `admin_02` 브랜치 병합 및 `.gitignore` 설정

**요청:** `main` 브랜치에 `admin_02`의 변경사항 병합.

**진행 과정:**
1.  이전에 완료되지 않은 merge 상태 발견 (`MERGE_HEAD exists`).
2.  `git commit`으로 보류 중이던 merge를 먼저 완료함.
3.  `git merge admin_02` 실행 결과, 이미 최신 상태(Already up to date)임을 확인.
4.  `git status`를 통해 추적되지 않는 파이썬 캐시 파일(`__pycache__`) 및 `db.sqlite3` 파일 발견.
5.  `.gitignore` 파일을 생성하여 불필요한 파일들을 Git 추적에서 제외하도록 설정.
6.  Git 인덱스에서 캐시된 파일들을 정리하는 과정에서 실수 발생. `git reset --hard HEAD~1` 명령어로 잘못된 commit을 되돌려 복구.
7.  올바른 절차에 따라 `.gitignore` 파일을 먼저 commit한 후, 추적에서 제외될 파일들을 인덱스에서 제거.
8.  `git status`로 작업 폴더가 깨끗한 상태임을 최종 확인.
9.  Gemini가 실행한 명령어 로그를 `DEVEOPMENT_GEMINI_LOG.md`에 별도로 생성 및 기록.