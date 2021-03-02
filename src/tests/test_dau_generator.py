import pytest

import sys
import json
from src.dau_pipeline import generate_records

def test_generate_records():
    sample_JSON = {"0": {
    		"Course": {
    			"CourseProviderName": "DAU",
    			"DepartmentName": "Marine Corps",
    			"EducationalContext": "Non - Mandatory",
    			"CourseCode": "DHA-US639",
    			"CourseTitle": "International Acquisition Integration",
    			"CourseDescription": "Once your presentation is done, you can save and print it. Discover how to save and recover presentations, use the undo and redo functions, save as a PDF, and print presentations.",
    			"CourseAudience": "SCI-Cleared personnel",
    			"CourseSectionDeliveryMode": "Live"
    		},
    		"Lifecycle": {
    			"Provider": "Defense Language Institute (DLI) || 1759 Lewis Rd., Monterey, CA, 93944 || 831-242-6936",
    			"Maintainer": "Keith Maj Eric J, MAWTS-1, Attn:  C3 Dept",
    			"OtherRole": "Success Factors LMS v. 1881"
            }
        }
    }

	target_JSON = {
    "_id": "0",
	"Course": {
    			"CourseProviderName": "DAU",
    			"DepartmentName": "Marine Corps",
    			"EducationalContext": "Non - Mandatory",
    			"CourseCode": "DHA-US639",
    			"CourseTitle": "International Acquisition Integration",
    			"CourseDescription": "Once your presentation is done, you can save and print it. Discover how to save and recover presentations, use the undo and redo functions, save as a PDF, and print presentations.",
    			"CourseAudience": "SCI-Cleared personnel",
    			"CourseSectionDeliveryMode": "Live"
    		},
    "Lifecycle": {
    			"Provider": "Defense Language Institute (DLI) || 1759 Lewis Rd., Monterey, CA, 93944 || 831-242-6936",
    			"Maintainer": "Keith Maj Eric J, MAWTS-1, Attn:  C3 Dept",
    			"OtherRole": "Success Factors LMS v. 1881"
            }
        }
    assert next(generate_records(sample_JSON)) == target_JSON
