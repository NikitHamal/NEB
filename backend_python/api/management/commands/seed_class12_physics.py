import json
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from api.models import SyllabusContent


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "class12_physics_from_physics_compressed.json"


class Command(BaseCommand):
    help = (
        "Seed the structured Class 12 Physics syllabus converted from "
        "Physics_compressed.pdf, including formulas, source pages and interactive blocks."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite chapters with matching chapter_id values.",
        )
        parser.add_argument(
            "--resource-id",
            default="",
            help=(
                "Optional Library Resource UUID for the uploaded source PDF. "
                "When supplied, source-page chips link back to the PDF reader."
            ),
        )
        parser.add_argument(
            "--data-file",
            default=str(DATA_FILE),
            help="Override the packaged structured syllabus JSON file.",
        )

    def handle(self, *args, **options):
        data_file = Path(options["data_file"]).expanduser().resolve()
        if not data_file.exists():
            raise CommandError(f"Physics syllabus data file not found: {data_file}")

        try:
            payload = json.loads(data_file.read_text(encoding="utf-8"))
        except Exception as exc:
            raise CommandError(f"Could not read physics syllabus JSON: {exc}") from exc

        if not isinstance(payload, list) or not payload:
            raise CommandError("Physics syllabus data must be a non-empty JSON array.")

        overwrite = bool(options["overwrite"])
        resource_id = (options.get("resource_id") or "").strip()[:36]
        now = int(time.time() * 1000)
        created = updated = skipped = 0

        for item in payload:
            chapter_id = str(item.get("chapter_id", "")).strip()
            if not chapter_id:
                self.stderr.write("Skipping row without chapter_id")
                skipped += 1
                continue

            defaults = {
                "grade_level": str(item.get("grade_level") or "Class 12").strip(),
                "subject": str(item.get("subject") or "Physics").strip(),
                "chapter_title": str(item.get("chapter_title") or chapter_id).strip(),
                "text_content": str(item.get("text_content") or ""),
                "question_answers": str(item.get("question_answers") or ""),
                "rich_content": item.get("rich_content") if isinstance(item.get("rich_content"), dict) else {},
                "source_resource_id": resource_id or str(item.get("source_resource_id") or "").strip()[:36],
                "source_label": str(item.get("source_label") or "Physics_compressed.pdf").strip()[:255],
                "order": int(item.get("order") or 0),
                "updated_at": now,
            }

            existing = SyllabusContent.objects.filter(chapter_id=chapter_id).first()
            if existing and not overwrite:
                skipped += 1
                self.stdout.write(f"Skipped: {existing.chapter_title}")
                continue

            if existing:
                for field, value in defaults.items():
                    setattr(existing, field, value)
                existing.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Updated: {existing.chapter_title}"))
            else:
                SyllabusContent.objects.create(
                    id=chapter_id,
                    chapter_id=chapter_id,
                    created_at=now,
                    **defaults,
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {defaults['chapter_title']}"))

        suffix = f" Linked source resource: {resource_id}." if resource_id else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created}, updated {updated}, skipped {skipped}.{suffix}"
            )
        )
