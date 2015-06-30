"""
Update a json document with a .json file of the following format:
{
    "READGROUP": "2013-2457_140122_SN673_0209_BC3E7WACXX_2",
    "DELETE_FIELDS": [
        "coverage1",
        "coverage2",
        "coverage8",
        "fraction_coverage1",
        "fraction_coverage2",
        "fraction_coverage8",
        "aligned_target_enrichment",
        "sequenced_target_enrichment"
    ],
    "ADD_FIELDS": {
        "some_field_name": "value",
        "another_field_name": "value",
        "coverage": {
            "V3_capture_t1": {
                "target_size": 6500000,
                "average": 976,
                "%covered_at_average": 0.4988,
                "90%": 302,
                "50%": 955,
                "10%": 1581,
                "zero_cov_bp": 41075,
                "%zero_cov": 0.0162
            },
            "V3_capture_t2": {
                "target_size": 3000000,
                "average": "550",
                "%covered_at_average": "0.4718",
                "90%": "114",
                "50%": "527",
                "10%": "960",
                "zero_cov_bp": "66662",
                "%zero_cov": "0.0194"
            }
        }
    }
}

Usage:
    update_document.py -j json [-d dry-run]

Options:
    -j json         .json Document containing
    -d dry-run      Run without committing any changes to Database
"""
__author__ = 'jgrundst'
from docopt import docopt


def main():
    args =  docopt(__doc__)
    print args


if __name__ == '__main__':
    main()