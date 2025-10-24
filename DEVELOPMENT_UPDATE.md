# 개발 업데이트 (2025-10-23)

## 1. 관리자 페이지 기능 개선 및 오류 수정

### 동적 설정 기능 추가
- **내용:** 관리자 페이지에서 '최대 파일 크기'와 'IP당 최대 파일 개수'를 슬라이더 UI로 직접 수정하고 적용할 수 있는 기능을 추가했습니다.
- **구현:**
    - `GlobalSettings` 데이터베이스 모델을 새로 생성하여 설정값을 영구적으로 저장 (`cloud_storage/models.py`).
    - `admin_page_view`가 POST 요청을 통해 들어온 설정값을 데이터베이스에 저장하도록 수정 (`cloud_storage/views.py`).
    - `upload_view`가 고정된 값이 아닌, 데이터베이스에 저장된 동적 설정값을 기준으로 업로드를 제한하도록 변경 (`cloud_storage/views.py`).
    - 관리자 페이지에 슬라이더와 '적용' 버튼을 포함한 폼을 추가 (`cloud_storage/templates/cloud_storage/admin_page.html`).
- **영향:** 하드코딩된 설정을 관리자가 웹 UI를 통해 직접 제어할 수 있게 되어 유연성이 크게 향상되었습니다.

### 템플릿 문법 오류 (TemplateSyntaxError) 수정
- **문제:** 관리자 페이지 접근 시, 템플릿 내에서 직접적인 나누기 연산(`{{ value / 1024 }}`)을 수행하여 `TemplateSyntaxError`가 발생했습니다.
- **해결:** 연산 로직을 템플릿에서 뷰(`admin_page_view`)로 이동시키고, 템플릿은 계산된 값만 받아서 표시하도록 수정했습니다. (`cloud_storage/views.py`, `cloud_storage/templates/cloud_storage/admin_page.html`)

### 파일 삭제 기능 오류 (NameError) 수정
- **문제:** 관리자 페이지에서 파일 삭제 버튼 클릭 시, `os` 모듈이 import되지 않아 `NameError: name 'os' is not defined` 오류가 발생했습니다.
- **해결:** `cloud_storage/views.py` 파일 상단에 `import os` 구문을 추가하여 문제를 해결했습니다.

## 2. 관리자 페이지 보안 강화

- **문제:** 관리자 페이지의 URL을 아는 경우, 별도의 인증 절차 없이 누구나 직접 접근할 수 있는 보안 취약점이 존재했습니다.
- **해결:** Django 세션(Session)을 이용한 인증 메커니즘을 도입했습니다.
    1.  **인증:** 특정 파일(`key`) 업로드 성공 시, 사용자의 세션에 관리자임을 나타내는 `is_admin` 플래그를 설정 (`cloud_storage/views.py` - `upload_view`).
    2.  **권한 확인:** 관리자 페이지 및 파일 삭제 기능 접근 시, `is_admin` 세션 플래그를 확인하여 권한이 없는 사용자는 메인 페이지로 리디렉션 (`cloud_storage/views.py` - `admin_page_view`, `delete_file_view`).
    3.  **로그아웃:** 관리자 페이지에 '로그아웃' 버튼을 추가하여, 클릭 시 세션의 관리자 플래그를 제거하고 안전하게 세션을 종료하는 기능을 구현 (`cloud_storage/views.py`, `cloud_storage/urls.py`, `cloud_storage/templates/cloud_storage/admin_page.html`).

## 3. Git 저장소 관리

- **`.gitignore` 설정:** `__pycache__` 디렉토리, `db.sqlite3` 데이터베이스 파일 등 프로젝트와 직접 관련이 없는 파일들이 Git 추적에서 제외되도록 `.gitignore` 파일을 생성하고 적용했습니다.
- **Commit:** 상기 변경사항들을 `feat: Add user authentication with Gemini CLI` 등의 메시지와 함께 commit하여 저장소에 반영했습니다.

# 개발 업데이트 (2025-10-24)

## 1. UI/UX 개선 및 디자인 시스템 도입

- **반응형 디자인 적용:**
  - 모든 페이지(`index`, `upload`, `admin_page`)에 Bootstrap의 Grid System (`row`, `col-md-*`)을 적용하여 모바일, 태블릿, 데스크톱 등 다양한 화면 크기에 최적화된 레이아웃을 구현했습니다.
- **Google Drive 스타일 시스템 도입:**
  - **`base.html` 템플릿 생성:** 모든 페이지가 상속받는 기본 템플릿을 도입하여 전체적인 디자인 일관성을 확보했습니다. 헤더, 푸터, 기본 스타일시트 등을 포함합니다.
  - **`static/css/style.css` 추가:** Google의 머티리얼 디자인 가이드라인을 참고하여 새로운 CSS 스타일시트를 작성했습니다. 색상 팔레트, 폰트(Roboto), 버튼, 카드, 입력 폼 등 전반적인 UI 요소에 통일된 디자인을 적용하여 사용자 경험을 향상시켰습니다.

## 2. 신규 기능 추가

- **오래된 파일 자동 삭제 기능:**
  - **모델 확장:** `GlobalSettings` 모델에 파일 보관 기간을 설정하는 `auto_delete_days` 필드를 추가했습니다.
  - **관리자 설정:** 관리자 페이지에서 파일 보관 기간(0~30일)을 슬라이더로 설정할 수 있는 UI를 추가했습니다. (0일은 비활성화)
  - **삭제 명령어:** `delete_old_files` Management Command를 구현하여, 설정된 기간이 지난 파일들을 서버에서 자동으로 삭제할 수 있는 기능을 추가했습니다. 이 명령어는 스케줄러를 통해 주기적으로 실행되어야 합니다.
- **최대 파일 저장 개수 제한 기능:**
  - **모델 확장:** `GlobalSettings` 모델에 전체 파일 저장 개수를 제한하는 `max_total_files` 필드를 추가했습니다.
  - **관리자 설정:** 관리자 페이지에서 최대 저장 개수(1~100개)를 슬라이더로 설정하는 UI를 추가했습니다.
  - **업로드 제한:** 파일 업로드 시, 현재 저장된 파일 총 개수가 설정된 최대치를 초과할 경우 업로드를 막는 로직을 `upload_view`에 추가했습니다.
- **About 페이지 추가:**
  - 사이트의 목적과 주요 기능을 설명하는 `about.html` 페이지와 관련 `view`, `url`을 추가하고 헤더를 통해 쉽게 접근할 수 있도록 링크를 추가했습니다.

## 3. 버그 수정 및 보안 강화

- **`NameError` 수정:** 파일 업로드 시 `uuid` 및 `urllib.parse` 모듈이 import되지 않아 발생하던 `NameError`를 `views.py`에 해당 모듈을 import하여 해결했습니다.
- **다운로드 보안 강화 (Brute-force 방지):**
  - **기능:** 다운로드 시 비밀번호를 5회 연속으로 잘못 입력한 IP에 대해 5분간 다운로드 시도를 차단하는 기능을 구현했습니다.
  - **구현:** Django의 Cache Framework(`LocMemCache`)를 사용하여 IP별 실패 횟수를 기록하고, 시간 제한을 설정했습니다.
- **`Page not found` (404) 오류 수정:**
  - **문제:** 존재하지 않는 파일 번호로 다운로드 시도 시, `get_object_or_404`로 인해 404 오류 페이지가 표시되었습니다.
  - **해결:** `download_view`에서 `try-except UploadedFile.DoesNotExist` 구문을 사용하여 예외를 직접 처리하고, 사용자에게 "잘못된 파일 번호입니다." 라는 명확한 오류 메시지를 다운로드 페이지에 표시하도록 수정했습니다.

## 4. 프로젝트 구조 및 관리 개선

- **`src` 디렉토리 구조 도입:**
  - Django 앱(`cloud_storage`)과 프로젝트(`TempCloud`)를 `src` 디렉토리 하위로 이동하여 소스 코드와 프로젝트 설정 파일을 분리했습니다.
  - `manage.py`와 `settings.py`의 경로 관련 설정을 수정하여 새로운 구조에 맞게 프로젝트가 정상적으로 동작하도록 변경했습니다.
- **`README.md` 상세화:**
  - 프로젝트 전체를 분석하여 주요 기능, 기술 스택, 설치 및 실행 방법(`Getting Started`), 사용법, 관리 명령어 등 상세한 내용을 포함하여 `README.md` 파일을 전면 업데이트했습니다.
- **`requirements.txt` 정리:**
  - `pip freeze`를 통해 생성된 `requirements.txt` 파일에서 프로젝트와 무관한 `pygame` 라이브러리를 제거하여 의존성을 명확하게 정리했습니다.