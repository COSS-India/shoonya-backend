from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .resources import (
    DatasetInstanceResource,
    SentenceTextResource,
    TranslationPairResource,
    OCRResource,
    BlockTextResource,
    ConversationResource,
    SpeechConversationResource,
)
from .models import (
    DatasetInstance,
    SentenceText,
    TranslationPair,
    OCRDocument,
    BlockText,
    Conversation,
    SpeechConversation,
)


@admin.register(DatasetInstance)
class DatasetInstanceAdmin(ImportExportActionModelAdmin):
    resource_class = DatasetInstanceResource

    list_display = (
        "instance_name",
        "dataset_type",
        "organisation_id",
        "public_to_managers",
        "parent_instance_id",
    )
    list_filter = ("dataset_type", "public_to_managers", "organisation_id")
    search_fields = ("instance_name", "instance_description")
    ordering = ("instance_name",)
    filter_horizontal = ("users",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "instance_name",
                    "instance_description",
                    "dataset_type",
                    "organisation_id",
                    "parent_instance_id",
                    "public_to_managers",
                    "users",
                )
            },
        ),
    )


@admin.register(SentenceText)
class SentenceTextAdmin(ImportExportActionModelAdmin):
    resource_class = SentenceTextResource

    list_display = ("id", "instance_id", "language", "domain", "quality_status")
    list_filter = ("language", "domain", "quality_status")
    search_fields = ("text", "corrected_text")
    ordering = ("id",)
    list_per_page = 50

    fieldsets = (
        (None, {"fields": ("instance_id", "language", "domain", "quality_status")}),
        ("Content", {"fields": ("text", "context", "corrected_text")}),
        ("Metadata", {"fields": ("metadata_json", "draft_data_json"), "classes": ("collapse",)}),
    )


@admin.register(TranslationPair)
class TranslationPairAdmin(ImportExportActionModelAdmin):
    resource_class = TranslationPairResource

    list_display = (
        "id",
        "instance_id",
        "input_language",
        "output_language",
        "domain",
        "rating",
        "labse_score",
    )
    list_filter = ("input_language", "output_language", "domain")
    search_fields = ("input_text", "output_text", "machine_translation")
    ordering = ("id",)
    list_per_page = 50

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "instance_id",
                    "input_language",
                    "output_language",
                    "domain",
                    "rating",
                    "labse_score",
                )
            },
        ),
        (
            "Content",
            {"fields": ("input_text", "output_text", "machine_translation", "context")},
        ),
        ("Metadata", {"fields": ("metadata_json", "draft_data_json"), "classes": ("collapse",)}),
    )


@admin.register(OCRDocument)
class OCRDocumentAdmin(ImportExportActionModelAdmin):
    resource_class = OCRResource

    list_display = (
        "id",
        "instance_id",
        "language",
        "file_type",
        "ocr_type",
        "ocr_domain",
        "page_number",
    )
    list_filter = ("language", "file_type", "ocr_type", "ocr_domain")
    search_fields = ("file_url", "image_url")
    ordering = ("id",)
    list_per_page = 50

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "instance_id",
                    "language",
                    "file_type",
                    "ocr_type",
                    "ocr_domain",
                    "page_number",
                    "file_url",
                    "image_url",
                )
            },
        ),
        (
            "Annotations",
            {
                "fields": (
                    "ocr_transcribed_json",
                    "ocr_prediction_json",
                    "annotated_document_details_json",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Advanced",
            {
                "fields": (
                    "image_details_json",
                    "bboxes_relation_json",
                    "bboxes_relation_prediction_json",
                    "metadata_json",
                    "draft_data_json",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(BlockText)
class BlockTextAdmin(ImportExportActionModelAdmin):
    resource_class = BlockTextResource

    list_display = ("id", "instance_id", "language", "domain")
    list_filter = ("language", "domain")
    search_fields = ("text", "splitted_text")
    ordering = ("id",)
    list_per_page = 50

    fieldsets = (
        (None, {"fields": ("instance_id", "language", "domain")}),
        ("Content", {"fields": ("text", "splitted_text", "splitted_text_prediction")}),
        ("Metadata", {"fields": ("metadata_json", "draft_data_json"), "classes": ("collapse",)}),
    )


@admin.register(Conversation)
class ConversationAdmin(ImportExportActionModelAdmin):
    resource_class = ConversationResource

    list_display = (
        "id",
        "instance_id",
        "language",
        "domain",
        "speaker_count",
        "conversation_quality_status",
    )
    list_filter = ("language", "domain", "conversation_quality_status")
    search_fields = ("topic", "scenario", "prompt")
    ordering = ("id",)
    list_per_page = 50

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "instance_id",
                    "language",
                    "domain",
                    "speaker_count",
                    "conversation_quality_status",
                )
            },
        ),
        ("Content", {"fields": ("topic", "scenario", "prompt", "speakers_json")}),
        (
            "Conversation Data",
            {
                "fields": (
                    "conversation_json",
                    "machine_translated_conversation_json",
                    "unverified_conversation_json",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("metadata_json", "draft_data_json"), "classes": ("collapse",)}),
    )


@admin.register(SpeechConversation)
class SpeechConversationAdmin(ImportExportActionModelAdmin):
    resource_class = SpeechConversationResource

    list_display = (
        "id",
        "instance_id",
        "language",
        "domain",
        "speaker_count",
        "audio_duration",
    )
    list_filter = ("language", "domain")
    search_fields = ("scenario", "reference_raw_transcript", "audio_url")
    ordering = ("id",)
    list_per_page = 50

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "instance_id",
                    "language",
                    "domain",
                    "speaker_count",
                    "audio_url",
                    "audio_duration",
                )
            },
        ),
        ("Content", {"fields": ("scenario", "speakers_json", "reference_raw_transcript")}),
        (
            "Transcription",
            {
                "fields": (
                    "transcribed_json",
                    "machine_transcribed_json",
                    "prediction_json",
                    "final_transcribed_json",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("metadata_json", "draft_data_json"), "classes": ("collapse",)}),
    )
