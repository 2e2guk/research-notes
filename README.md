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

기본 검색은 제목과 글의 짧은 설명을 대상으로 합니다. 라이트/다크 전환, 수식과 클릭 이미지 확대 기능을 활성화했습니다.
초안은 배포되지 않습니다. `_drafts/paper-review.md`를 복사해 날짜가 붙은 파일로 `_posts/`에 저장하면 공개 글이 됩니다.
그림 예시 마크업은 실제 그림을 넣은 뒤 사용하세요.
첫 글을 게시한 뒤 소개 화면에도 최근 글을 표시하려면 `_pages/about.md`에서 `latest_posts.enabled`를 `true`로 바꾸세요.

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
