**Bash (Linux / macOS / Git Bash / WSL):**

```bash
# Повысить patch-версию (0.1.4 → 0.1.5), закоммитить, создать тег и отправить
./scripts/release.sh patch

# Повысить minor (0.1.4 → 0.2.0) и создать GitHub Release (запустится публикация в PyPI)
./scripts/release.sh minor --release

# Установить явную версию, только обновить файлы (без git)
./scripts/release.sh 0.2.0 --no-git

# Показать, что будет сделано, без изменений
./scripts/release.sh patch --dry-run
```

**PowerShell (Windows):**

```powershell
.\scripts\release.ps1 patch
.\scripts\release.ps1 minor -Release
.\scripts\release.ps1 0.2.0 -NoGit
.\scripts\release.ps1 patch -DryRun
```

| Аргумент | Описание |
|----------|----------|
| `patch` \| `minor` \| `major` \| `X.Y.Z` | Тип повышения версии или новая версия |
| `--no-git` / `-NoGit` | Только обновить файлы, без коммита, тега и push |
| `--release` / `-Release` | После push создать GitHub Release через `gh` (запустится workflow публикации в PyPI) |
| `--dry-run` / `-DryRun` | Показать планируемые действия без изменений |

Для `--release` нужен установленный и авторизованный [GitHub CLI](https://cli.github.com/) (`gh`). Перед первым запуском `.sh` выполните: `chmod +x scripts/release.sh`.

**Связь с CHANGELOG:** при создании GitHub Release (`--release` / `-Release`) скрипт ищет в корне репозитория файл `CHANGELOG.md` и, если в нём есть секция с новой версией (например, `## [1.2.7]` или `## [1.2.7](url)`), подставляет её текст как описание релиза. Если секции нет — используются сгенерированные GitHub заметки. Рекомендуемый порядок: добавить в `CHANGELOG.md` блок для следующей версии, затем выполнить `release.sh patch --release` (или `minor`/`major`).
