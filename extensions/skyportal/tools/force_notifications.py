import argparse
import sys

parser = argparse.ArgumentParser(
    description='Force user notifications to certain settings', add_help=True
)
parser.add_argument('--user_ids', help='Comma-separated list of user IDs to change notification preferences for. Or "*" to change all users.')
parser.add_argument('--list', action='store_true', help='List all users and their notification preferences')
parser.add_argument('--prettyprint', action='store_true', help='Do not list notification preferences when using --list', default=False)
parser.add_argument('--only_missing_email', action='store_true', help='Only list users with missing email addresses', default=False)

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

from copy import deepcopy
import sqlalchemy as sa  # noqa: E402
from baselayer.app.env import load_env  # noqa: E402
from baselayer.app.models import init_db, User, DBSession  # noqa: E402
from baselayer.app.config import recursive_update

env, cfg = load_env()
init_db(**cfg['database'])

BOLD = '\033[1m'
END = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'

preferences = {
    "notifications": {
				"sources": {
					"email": {
						"active": True
					},
					"active": True,
					"classifications": [
						"Kilonova Candidate",
                        "GO GRANDMA",
                        "GO GRANDMA (HIGH PRIORITY)",
                        "STOP GRANDMA",
					]
				},
				"gcn_events": {
					"email": {
						"active": True
					},
					"active": True,
					"gcn_tags": [],
					"gcn_notice_types": [
						"SWIFT_BAT_GRB_POS_ACK",
						"SWIFT_XRT_POSITION",
                        "SWIFT_BAT_GRB_LC",
					]
				}
			}
}

for k, v in preferences.items():
	if isinstance(v, dict):
		preferences[k] = {key: val for key, val in v.items() if val != ""}

def set_user_notification_preference(user_ids=None):
	with DBSession() as session:
		if user_ids == '*':
			users = session.scalars(sa.select(User)).all()
		else:
			user_ids = [int(user_id) for user_id in user_ids.split(',')]
			users = session.scalars(sa.select(User).where(User.id.in_(user_ids))).all()
		for user in users:
			user_prefs = deepcopy(user.preferences)
			if not user_prefs:
				user_prefs = preferences
			else:
				user_prefs = recursive_update(user_prefs, preferences)
			user.preferences = user_prefs

		session.commit()

def get_users(only_missing_email=False):
	with DBSession() as session:
		if only_missing_email:
			users = session.scalars(sa.select(User).where(User.contact_email == None)).all()
		else:
			users = session.scalars(sa.select(User)).all()
	return users

def list_user_notifications_preferences(prettyprint=False, only_missing_email=False):
	users = get_users(only_missing_email=only_missing_email)
	if len(users) == 0:
		print('\nNo users in database')
	else:
		# print each user's username and roles
		print(f'\n{BOLD}List of users and current roles:{END}')
		# sort users by id
		users.sort(key=lambda x: x.id)
		for i, user in enumerate(users):
			notifications_prefs = user.preferences['notifications'] if "notifications" in user.preferences else None
			missing_email_str = f" {RED}(no email){END}" if user.contact_email is None else " "
			print(f'\nid:{BOLD}{user.id}. {YELLOW}{user.username}{END}{missing_email_str} has the following preferences:\n')
			# pretty print user preferences
			if prettyprint:
				for k, v in notifications_prefs.items():
					if isinstance(v, dict):
						print(f'{k}:')
						for k2, v2 in v.items():
							if isinstance(v2, dict):
								print(f'  {k2}:')
								for k3, v3 in v2.items():
									print(f'    {k3}: {v3}')
							else:
								print(f'  {k2}: {v2}')
					else:
						print(f'{k}: {v}')
			else:
				print(notifications_prefs)

def main():
	if args.list or args.user_ids:
		if args.list:
			list_user_notifications_preferences(prettyprint=args.prettyprint, only_missing_email=args.only_missing_email)
		if args.user_ids:
			set_user_notification_preference(user_ids=args.user_ids)
	else:
		print(
			f'\n{BOLD}{RED}No arguments given;{END} printing {BOLD}{GREEN}help{END}:\n'
		)
		parser.print_help()

if __name__ == '__main__':
	main()
