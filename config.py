"""
File contains Constant variables
"""

import os

TASK_NAME = "Task_ING_summary"

LOGS_FOLDER = "logs"
FILES_FOLDER = "files"
MAPPING_FOLDER = "mapping"

CATEGORIES_MAPPING = os.path.join(FILES_FOLDER, MAPPING_FOLDER, "category_mapping.json")
FIELD_MAPPING = os.path.join(FILES_FOLDER, MAPPING_FOLDER, "field_mapping.json")
UNCATEGORISED = os.path.join(FILES_FOLDER, "uncategorised")
INTPUT_FOLDER = os.path.join(FILES_FOLDER, "input")
OUTPUT_FOLDER = os.path.join(FILES_FOLDER, "output")
