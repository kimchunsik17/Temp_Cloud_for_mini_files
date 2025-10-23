프로젝트: 임시 파일 클라우드 (Gemini CLI)

1. 프로젝트 개요

목표: 과제(PPT, Word 등)와 같이 작은 파일들을 임시로 저장하고, 어디서든 쉽게 접근할 수 있는 간단한 클라우드 스토리지 웹사이트를 구축합니다.

핵심 기능: 고유한 '파일 번호'와 '4자리 비밀번호'만으로 파일 업로드 및 다운로드를 지원합니다.

기술 스택: Django (Template), Bootstrap 5

개발 환경: Gemini CLI

2. 핵심 기능 상세

파일 업로드:

사용자가 메인 페이지에서 '파일 업로드'를 선택합니다.

파일과 함께 사용할 4자리 숫자 비밀번호를 입력합니다.

업로드 성공 시, 시스템은 해당 파일에 접근할 수 있는 고유한 파일 번호(예: 6자리 숫자 또는 랜덤 문자열)를 생성하여 사용자에게 보여줍니다.

파일 다운로드:

사용자가 메인 페이지에서 '파일 번호'와 '4자리 비밀번호'를 입력합니다.

두 정보가 모두 일치하는 경우에만 파일 다운로드 링크가 활성화됩니다.

파일 관리 (임시):

(고려 사항) 업로드된 파일은 서버 부담을 줄이기 위해 일정 시간(예: 24시간 또는 48시간) 후 자동으로 삭제되는 기능을 구현할 수 있습니다.

3. 개발 프로세스 및 Git 전략

이 프로젝트는 과제의 일부이므로, 주요 기능 구현 단계마다 Git 브랜치를 생성하여 변경 사항을 관리합니다.

main 브랜치: 최종적으로 안정화된 버전, 혹은 과제 제출 버전을 관리합니다.

develop 브랜치: main에서 분기하며, 개발의 중심이 되는 브랜치입니다.

기능 브랜치 (Feature Branches):

Gemini CLI를 통해 큰 변화(예: 모델 생성, 기본 뷰 설정)를 준 직후, 또는 새로운 기능을 추가하기 전에 develop 브랜치에서 새로 분기합니다.

브랜치 이름 규칙: feat/기능이름 (예: feat/file-upload-model, feat/bootstrap-layout, feat/download-logic)

작업이 완료되면 develop 브랜치로 Pull Request(PR)를 보내고 병합합니다.

예시 Git 워크플로우:

Gemini로 Django 프로젝트 기본 설정.

git checkout -b develop

Gemini로 파일 저장을 위한 기본 모델 생성.

(큰 변화 발생) git add . && git commit -m "feat: Add initial File model via Gemini"

git checkout -b feat/upload-view (업로드 뷰 및 템플릿 상세 작업 시작)

(작업 완료 후) git checkout develop && git merge feat/upload-view

4. Gemini CLI 명령어 기록

사용자와의 문답은 항상 DEVEOPMENT_GEMINI_LOG.md에 저장할 것.

=== 1. 프로젝트 초기 설정 ===
# (예시) Django 프로젝트 생성 (가정)
# gemini create django_project --name TempCloud --template bootstrap
# 
# === 2. 모델 생성 ===
# (예시) 파일 저장을 위한 모델 생성 요청
# gemini create django_model UploadedFile file:FileField password:CharField(max_length=4) file_id:CharField(max_length=10, unique=True) created_at:DateTimeField(auto_now_add=True)
#
# === 3. 템플릿 및 뷰 생성 ===
# (예시) 메인 페이지(다운로드 폼) 템플릿 생성
# gemini create django_template index.html --bootstrap --title "임시 파일 보관소" --body "파일 번호와 비밀번호 입력 폼"
#
# (예시) 메인 페이지 뷰 생성
# gemini create django_view index_view --template index.html --logic "파일 ID와 비밀번호를 받아 검증하는 로직"
#
# (예시) 파일 업로드 페이지 템플릿 및 뷰 생성
# gemini create django_view upload_view --template upload.html --logic "파일 업로드 폼 처리, 4자리 비밀번호 설정, 고유 file_id 생성 및 반환"
#
# === 4. URL 설정 ===
# (예시) URL 라우팅 설정 요청
# gemini update django_urls --add_path "" index_view --add_path "upload/" upload_view
#

