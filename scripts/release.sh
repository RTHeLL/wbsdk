#!/usr/bin/env bash
# Обновление версии и создание релиза (Bash).
# Использование: ./scripts/release.sh patch|minor|major|X.Y.Z [--no-git] [--release] [--dry-run]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYPROJECT="$REPO_ROOT/pyproject.toml"
INIT_PY="$REPO_ROOT/src/wbsdk/__init__.py"

# Переход в корень репозитория
cd "$REPO_ROOT"

if [[ ! -f "$PYPROJECT" ]]; then
  echo "Ошибка: pyproject.toml не найден в $REPO_ROOT" >&2
  exit 1
fi
if [[ ! -f "$INIT_PY" ]]; then
  echo "Ошибка: src/wbsdk/__init__.py не найден" >&2
  exit 1
fi

# Парсинг аргументов
BUMP_ARG=""
NO_GIT=false
DO_RELEASE=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --no-git)   NO_GIT=true ;;
    --release)  DO_RELEASE=true ;;
    --dry-run)  DRY_RUN=true ;;
    patch|minor|major)
      if [[ -n "$BUMP_ARG" ]]; then
        echo "Ошибка: указан повторный аргумент версии: $arg" >&2
        exit 1
      fi
      BUMP_ARG="$arg"
      ;;
    *)
      if [[ "$arg" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        if [[ -n "$BUMP_ARG" ]]; then
          echo "Ошибка: указан повторный аргумент версии: $arg" >&2
          exit 1
        fi
        BUMP_ARG="$arg"
      else
        echo "Неизвестный аргумент: $arg" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$BUMP_ARG" ]]; then
  echo "Использование: $0 patch|minor|major|X.Y.Z [--no-git] [--release] [--dry-run]" >&2
  exit 1
fi

# Текущая версия из pyproject.toml
CURRENT_VERSION=$(sed -n 's/^version = "\(.*\)"$/\1/p' "$PYPROJECT")
if [[ -z "$CURRENT_VERSION" ]]; then
  echo "Ошибка: не удалось прочитать version из pyproject.toml" >&2
  exit 1
fi

# Вычисление новой версии
compute_new_version() {
  local bump="$1"
  local current="$2"
  local major minor patch
  IFS=. read -r major minor patch <<< "$current"
  major=${major:-0}
  minor=${minor:-0}
  patch=${patch:-0}

  case "$bump" in
    patch)
      patch=$((patch + 1))
      echo "$major.$minor.$patch"
      ;;
    minor)
      minor=$((minor + 1))
      patch=0
      echo "$major.$minor.$patch"
      ;;
    major)
      major=$((major + 1))
      minor=0
      patch=0
      echo "$major.$minor.$patch"
      ;;
    *)
      # явная версия X.Y.Z
      if [[ "$bump" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "$bump"
      else
        echo "Ошибка: некорректная версия $bump" >&2
        return 1
      fi
      ;;
  esac
}

NEW_VERSION=$(compute_new_version "$BUMP_ARG" "$CURRENT_VERSION")
if [[ $? -ne 0 ]]; then
  exit 1
fi

echo "Текущая версия: $CURRENT_VERSION"
echo "Новая версия:  $NEW_VERSION"

if [[ "$DRY_RUN" == true ]]; then
  echo "[dry-run] Будет обновлено: pyproject.toml, src/wbsdk/__init__.py"
  if [[ "$NO_GIT" != true ]]; then
    echo "[dry-run] Будет: git add, commit «Bump version to $NEW_VERSION», tag v$NEW_VERSION, push"
  fi
  if [[ "$DO_RELEASE" == true ]]; then
    echo "[dry-run] Будет: gh release create v$NEW_VERSION --generate-notes"
  fi
  exit 0
fi

# Переносимая замена в файле (без sed -i из-за различий macOS/GNU)
replace_in_file() {
  local file="$1"
  local old_pattern="$2"
  local new_replacement="$3"
  local tmp_file
  tmp_file=$(mktemp)
  sed "s#$old_pattern#$new_replacement#" "$file" > "$tmp_file"
  mv "$tmp_file" "$file"
}

# Экранирование точек в версии для sed
CURRENT_ESC=$(echo "$CURRENT_VERSION" | sed 's/\./\\./g')

replace_in_file "$PYPROJECT" "^version = \"$CURRENT_ESC\"\$" "version = \"$NEW_VERSION\""
replace_in_file "$INIT_PY" "__version__ = \"$CURRENT_ESC\"" "__version__ = \"$NEW_VERSION\""

echo "Обновлены pyproject.toml и src/wbsdk/__init__.py"

if [[ "$NO_GIT" == true ]]; then
  echo "Флаг --no-git: git-операции пропущены."
  exit 0
fi

# Git: add, commit, tag, push
git add "$PYPROJECT" "$INIT_PY"
git commit -m "Bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
git push
git push --tags

if [[ "$DO_RELEASE" == true ]]; then
  if ! command -v gh &>/dev/null; then
    echo "Ошибка: gh (GitHub CLI) не найден. Установите gh и выполните авторизацию." >&2
    exit 1
  fi
  gh release create "v$NEW_VERSION" --generate-notes
  echo "GitHub Release v$NEW_VERSION создан. Workflow публикации в PyPI должен запуститься."
fi
