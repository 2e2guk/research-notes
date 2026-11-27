# Research Notes

이강욱의 논문 읽기 기록과 CV를 위한 GitHub Pages 사이트입니다.

- 테마: [al-folio v1.2](https://github.com/alshedivat/al-folio/releases/tag/v1.2)
- 원본 commit: `b95d6d61a1b0663529094b1b5f4fbe8aa41f8a04`
- 블로그 주소: https://2e2guk.github.io/research-notes/
- 기존 https://2e2guk.github.io/ 블로그와는 별도로 운영합니다.

## 수정할 파일

| 작업 | 파일 |
| --- | --- |
| 소개 | `_pages/about.md` |
| CV | `_data/cv.yml` |
| 논문 글 | `_posts/YYYY-MM-DD-title.md` |
| 글 초안 | `_drafts/paper-review.md` |
| 그림 | `assets/img/` |
| PDF | `assets/pdf/` |
| 사이트 설정 | `_config.yml` |
| 주제 이름·설명·순서 | `_data/topics.yml` |

기본 검색은 제목과 글의 짧은 설명을 대상으로 합니다. 라이트/다크 전환, 수식과 클릭 이미지 확대 기능을 활성화했습니다.
초안은 배포되지 않습니다. `_drafts/paper-review.md`를 복사해 날짜가 붙은 파일로 `_posts/`에 저장하면 공개 글이 됩니다.
그림 예시 마크업은 실제 그림을 넣은 뒤 사용하세요.
첫 글을 게시한 뒤 소개 화면에도 최근 글을 표시하려면 `_pages/about.md`에서 `latest_posts.enabled`를 `true`로 바꾸세요.

## 주제별 목차와 읽는 순서

첫 화면(`/`)은 주제별 목차입니다. `태그`는 주제에 관계없이 같은 태그의 글을 모으며, `전체 글`(`/blog/`)은 게시 날짜순의 보조 목록입니다. 소개는 `/about/`, CV는 `/cv/`에 있습니다.

글 파일 맨 위의 `---` 사이에 다음처럼 적습니다. 아래 예시는 사용법이며 공개 글이 아닙니다.

```yaml
---
layout: post
title: "OpenVLA의 행동 표현 이해하기"
description: "연속 행동을 action token으로 바꾸는 과정을 정리합니다."
topic: vla
series: OpenVLA 읽기
series_order: 20
tags: [VLA, 행동표현, 모방학습]
toc:
  sidebar: right
---
```

- **주제**: `topic`에 `_data/topics.yml`의 `id`를 적습니다. 현재 `vla`, `tactile`, `interpretability`가 있습니다. 새 주제는 이 파일에 항목을 추가하면 됩니다. 배열의 위아래 순서가 홈의 주제 순서입니다.
- **시리즈**: 같은 주제 안에서 `series` 이름이 같으면 하나로 묶입니다. 별도의 시리즈 등록은 필요 없습니다. 띄어쓰기를 포함해 같은 이름을 사용하세요. 시리즈 묶음끼리는 이름순으로 표시됩니다.
- **읽는 순서**: `series_order`에는 따옴표 없는 숫자를 적습니다. 작은 숫자가 먼저 보입니다. `10, 20, 30`처럼 간격을 두면 나중에 `15`를 넣기 쉽습니다. 같은 시리즈에서 순서 번호를 중복하지 않는 것을 권장합니다.
- **번호를 생략한 글**: 같은 시리즈의 번호 있는 글 다음에 놓입니다. 게시 날짜는 순서 지정과 별개로 유지됩니다.
- **시리즈를 생략한 글**: 그 주제의 ‘개별 기록’으로 모입니다. 주제를 생략했거나 등록되지 않은 `topic`을 적은 글은 ‘그 밖의 기록’에 남아 있어 사라지지 않습니다.
- **태그**: `tags`에 여러 값을 적으면 태그 목록과 각 태그의 글 목록이 자동 생성됩니다. 한글과 띄어쓰기도 사용할 수 있습니다. 같은 개념은 같은 표기로 유지하세요.

순서 변경은 글의 `series_order` 숫자를 수정하고 저장하면 됩니다. 파일 이름의 날짜나 실제 작성 날짜를 바꿀 필요가 없습니다. 드래그해서 순서를 바꾸는 관리 화면은 없습니다.

새 주제의 `id`에는 영문 소문자·숫자·하이픈을 사용하고, 서로 다른 주제에 같은 ID를 쓰지 마세요. `other`는 ‘그 밖의 기록’을 위해 예약되어 있습니다.

예를 들어 처음 두 글을 `10`, `30`으로 게시한 뒤, 나중에 추가한 선수 개념 글에 `20`을 주면 목차에서는 `10 → 20 → 30` 순서로 표시됩니다.

## 구조 검증

`python3 scripts/check_reading_navigation.py`는 별도 임시 폴더에 테스트 글을 만든 뒤 실제 Jekyll 빌드를 통해 숫자순 정렬, 누락 항목 처리와 태그 링크를 검증합니다. 테스트 글은 공개 저장소의 `_posts`나 배포 결과에 들어가지 않습니다.
정상 사이트를 빌드한 뒤 `python3 scripts/check_reading_navigation.py --production-dir _site`로 테스트 글이 배포 파일에 섞이지 않았는지도 확인합니다. GitHub Actions에서도 두 검사를 실행합니다.

CV PDF를 넣으려면 `assets/pdf/cv.pdf`에 저장하고 `_pages/cv.md`의 front matter에 `cv_pdf: /assets/pdf/cv.pdf`를 추가하세요.
학력, 경력, 소속은 사용자가 제공한 정보를 바탕으로 채웁니다.

## GitHub Pages

저장소 Settings → Pages → Build and deployment → Source를 **GitHub Actions**로 지정합니다.
`main`에 변경을 push하면 `.github/workflows/pages.yml`이 빌드한 후 Pages에 배포합니다.

## 로컬 실행

Ruby 3.3.5, Bundler 4.0.6, Node.js와 ImageMagick이 필요합니다.

```sh
bundle install
bundle exec jekyll serve
```

로컬 주소는 `http://localhost:4000/research-notes/`입니다.
