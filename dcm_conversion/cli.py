r"""Convert DICOMs to NIfTI files.

BIDs org, deface ...

Example
-------
python cli.py \
    --sub-list ER0009 \
    --raw-dir /mnt/keoki/experiments2/EmoRep/Emorep_BIDS/test
"""
# %%
import os
import sys
import glob
import textwrap
from argparse import ArgumentParser, RawTextHelpFormatter
from dcm_conversion import convert


def get_args():
    """Get and parse arguments."""
    parser = ArgumentParser(
        description=__doc__, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "--source-dir",
        default="/mnt/keoki/experiments2/EmoRep/Emorep_BIDS/sourcedata",
        help=textwrap.dedent(
            """\
            Path to DICOM parent directory "sourcedata"
            (default : %(default)s)
            """
        ),
        type=str,
    )
    parser.add_argument(
        "--raw-dir",
        default="/mnt/keoki/experiments2/EmoRep/Emorep_BIDS/rawdata",
        help=textwrap.dedent(
            """\
            Path to DICOM parent directory "rawdata"
            (default : %(default)s)
            """
        ),
        type=str,
    )

    required_args = parser.add_argument_group("Required Arguments")
    required_args.add_argument(
        "--sub-list",
        nargs="+",
        help=textwrap.dedent(
            """\
            List of subject IDs to submit for pre-processing,
            e.g. "--sub-list ER4414" or "--sub-list ER4414 ER4415 ER4416".
            """
        ),
        type=str,
        required=True,
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser


# %%
def main():
    """Title."""

    # for testing
    source_path = "/mnt/keoki/experiments2/EmoRep/Emorep_BIDS/sourcedata"
    raw_path = "/mnt/keoki/experiments2/EmoRep/Emorep_BIDS/test"
    sub_list = ["ER0009"]

    args = get_args().parse_args()
    source_path = args.source_dir
    raw_path = args.raw_dir
    sub_list = args.sub_list
    assert len(sub_list) == 1, "Only accepting one subject atm."

    for subj in sub_list:
        dcm_list = glob.glob(f"{source_path}/{subj}/day*/DICOM")
        print(dcm_list)
        for subj_source in dcm_list:
            sess_task = "ses-day" + subj_source.split("day")[1].split("/")[0]
            sess, task = sess_task.split("_")
            subj_raw = os.path.join(raw_path, f"sub-{subj}/{sess}")
            print(
                f"""\
                subj : {subj}
                subj_source : {subj_source}
                sess : {sess}
                task : {task}
                subj_raw : {subj_raw}
            """
            )
            # std_out, std_err = convert.dcm2niix(subj_source, subj_raw, subj, sess, task)
            # print(std_out)
            # print(std_err)


if __name__ == "__main__":
    main()
