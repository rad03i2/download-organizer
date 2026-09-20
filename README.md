# Download Organizer

A safe, local-first Python CLI for turning a cluttered Downloads folder into predictable file-type categories — with **preview-first behavior, SHA-256 change detection, collision-safe naming, transactional rollback, and undo manifests**.

> No cloud upload. No telemetry. No automatic deletion. The default command changes nothing until you explicitly pass `--apply`.

## Why this project exists
Downloads folders become noisy quickly, while aggressive cleanup scripts can overwrite or lose files. Download Organizer is deliberately conservative: it builds a deterministic plan, fingerprints each source, refuses changed files, avoids name collisions, and records every successful move so it can be undone.

## Features
- Categorizes Images, Videos, Audio, Documents, Spreadsheets, Presentations, Archives, Installers, Code, and Other files.
- Preview is the default; `--apply` is required to move anything.
- SHA-256 verifies a file did not change between preview and move.
- Existing destinations are never overwritten; `name (1).ext`, `name (2).ext`, etc. are chosen safely.
- Applied moves are rolled back if a later move fails.
- JSON manifest records every move and enables verified undo.
- Undo refuses to overwrite an occupied original path or restore a destination that changed after organization.
- Hidden files are skipped by default; symbolic links are never followed.
- Optional recursive scanning while already-organized category directories are ignored.
- JSON plan output for scripts and integrations.
- Cross-platform Python 3.10+ implementation with no runtime dependencies.

## Installation
```bash
git clone https://github.com/rad03i2/download-organizer.git
cd download-organizer
python -m pip install .
```
For development:
```bash
python -m pip install -e ".[dev]"
```

## Usage
Preview a Downloads folder (safe default):
```bash
download-organizer organize ~/Downloads
```
Apply the exact generated plan:
```bash
download-organizer organize ~/Downloads --apply
```
Choose a manifest location:
```bash
download-organizer organize ~/Downloads --apply --manifest ~/organize-backup.json
```
Undo later:
```bash
download-organizer undo ~/organize-backup.json
```
Recursive scan and machine-readable preview:
```bash
download-organizer organize ~/Downloads --recursive --json
```
Hidden files are included only when explicitly requested:
```bash
download-organizer organize ~/Downloads --include-hidden
```

## What happens on disk
`report.pdf` becomes `Downloads/Documents/report.pdf`; `photo.JPG` becomes `Downloads/Images/photo.JPG`. If `Documents/report.pdf` already exists, the incoming file becomes `report (1).pdf` instead of replacing it. On `--apply`, the default manifest is stored under `.download-organizer/` in the target folder.

## Python API
```python
from pathlib import Path
from download_organizer import build_plan, apply_plan

root = Path.home() / "Downloads"
plan = build_plan(root)
apply_plan(plan, root / ".download-organizer" / "my-run.json")
```

## Project structure
```text
src/download_organizer/
  __init__.py     Public API and version
  core.py         Discovery, planning, hashing, apply, rollback, undo
  cli.py          Command-line interface
tests/test_core.py
.github/workflows/ci.yml
```

## Testing
```bash
ruff check src tests
pytest -q
```
CI runs linting and tests on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Security & privacy
All processing is local. The application does not connect to the network, delete files, execute downloaded files, or follow symbolic links. SHA-256 here is an integrity guard, not malware scanning. Always keep independent backups of important data.

## Limitations
- Categories are extension-based, not content/MIME detection.
- The tool organizes regular files; it does not move directories.
- Undo intentionally stops when a destination changed or an original path is occupied rather than guessing.
- Concurrent external modifications can still race with filesystem operations; important data should always be backed up.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Security guidance is in [SECURITY.md](SECURITY.md).

## License
MIT License — see [LICENSE](LICENSE).

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

# منظم التنزيلات — Download Organizer

أداة Python محلية وآمنة لتنظيم مجلد التنزيلات إلى تصنيفات واضحة حسب نوع الملف، مع **المعاينة قبل التنفيذ، والتحقق ببصمة SHA-256، ومنع استبدال الملفات، والتراجع عند فشل العملية، وإمكانية Undo عبر ملف Manifest**.

> لا رفع سحابي، لا تتبع، لا حذف تلقائي. الوضع الافتراضي هو المعاينة فقط، ولن تُنقل الملفات إلا عند استخدام `--apply` صراحةً.

## لماذا هذا المشروع؟
يتحول مجلد التنزيلات بسرعة إلى مكان مزدحم، بينما قد تتسبب سكربتات التنظيف البسيطة باستبدال ملفات مهمة. لذلك صُممت الأداة لتكون محافظة: تبني خطة واضحة أولًا، تتحقق من أن الملف لم يتغير، تمنع تعارض الأسماء، وتسجل كل عملية نقل ناجحة كي يمكن عكسها.

## الميزات
- تصنيف الصور والفيديو والصوت والمستندات والجداول والعروض والأرشيفات والمثبتات والكود والملفات الأخرى.
- المعاينة هي الوضع الافتراضي، والتنفيذ يحتاج `--apply`.
- التحقق من الملف ببصمة SHA-256 قبل نقله.
- عدم استبدال أي ملف موجود؛ يتم اختيار اسم آمن مثل `file (1).pdf`.
- Rollback تلقائي للملفات المنقولة إذا فشلت خطوة لاحقة.
- Manifest بصيغة JSON لكل عملية مطبقة مع دعم التراجع.
- Undo يرفض الكتابة فوق مسار أصلي مشغول أو إعادة ملف تم تعديله بعد التنظيم.
- تجاهل الملفات المخفية افتراضيًا وعدم اتباع الروابط الرمزية.
- دعم الفحص المتكرر للمجلدات مع تجاهل مجلدات التصنيف المنظمة مسبقًا.
- إخراج خطة JSON للاستخدام البرمجي.
- يعمل على Python 3.10+ بلا تبعيات تشغيل خارجية.

## التثبيت
```bash
git clone https://github.com/rad03i2/download-organizer.git
cd download-organizer
python -m pip install .
```
للتطوير والاختبار:
```bash
python -m pip install -e ".[dev]"
```

## الاستخدام
معاينة فقط:
```bash
download-organizer organize ~/Downloads
```
تنفيذ التنظيم:
```bash
download-organizer organize ~/Downloads --apply
```
تحديد ملف Manifest ثم التراجع لاحقًا:
```bash
download-organizer organize ~/Downloads --apply --manifest ~/organize-backup.json
download-organizer undo ~/organize-backup.json
```
فحص متكرر وإخراج JSON:
```bash
download-organizer organize ~/Downloads --recursive --json
```

## الأمان والخصوصية
كل المعالجة محلية. البرنامج لا يتصل بالإنترنت، ولا يحذف الملفات، ولا يشغّل الملفات التي تم تنزيلها، ولا يتبع الروابط الرمزية. استخدام SHA-256 هنا للتحقق من سلامة الملف أثناء سير العمل وليس لفحص البرمجيات الخبيثة. احتفظ دائمًا بنسخة احتياطية مستقلة للملفات المهمة.

## الاختبارات
```bash
ruff check src tests
pytest -q
```
يختبر GitHub Actions المشروع على Ubuntu وWindows وmacOS باستخدام Python 3.10 و3.12 و3.13.

## القيود
- التصنيف يعتمد على امتداد الملف وليس تحليل المحتوى الفعلي.
- الأداة تنظم الملفات العادية ولا تنقل المجلدات.
- التراجع يتوقف عمدًا عند وجود تعارض أو تعديل بدل اتخاذ قرار قد يؤدي إلى فقدان بيانات.
- لا يمكن لأي أداة ملفات إلغاء جميع مخاطر التعديلات المتزامنة؛ النسخ الاحتياطي مهم للبيانات الحساسة.

## المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة و[SECURITY.md](SECURITY.md) لإرشادات الأمان. المشروع مرخص برخصة MIT الموجودة في [LICENSE](LICENSE).

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
