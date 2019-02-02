import argparse
import json
import sys

sys.path.append("..")

from utils.db_session import session as db_session
from utils.models import VKGroupBase


def main(filepath):
    sess = db_session()

    with open(filepath, 'r') as file:
        groups_info = json.load(file)

        for group in groups_info:
            sess.add(VKGroupBase(
                group_id=group['id'],
                group_name=group['name'],
                is_closed=group['is_closed'],
                is_deactivated=True if group.get('deactivated') else False,
                group_type=group['type'],
                members_count=group.get('members_count', 0),
                trending=group.get('trending', 0),
                wall=group.get('wall', 0)
                )
            )
        sess.commit()
        sess.close()

    print(f'Operation took {str(time.clock() - start_time)} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", help="Path to the JSON file")
    args = parser.parse_args()
    if args.filepath:
        main(args.filepath)
    else:
        main('C:\projects\ProjectInsta\ProjectInsta_TR\dbdata\mt_group_info.json')
