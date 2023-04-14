""" Helper """
from datetime import datetime,timedelta
import argparse
import string
import secrets
import json

alphabet = string.ascii_letters + string.digits

result_json = {
  "game_config": {
    "flag_lifetime": 3,
    "round_time": 30,
    "game_start": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000"),
    "game_end": (datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S.000000"),
    "default_score": 2500,
    "quant_point": 100
  },
  "teams": [],
  "services": []
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Jury helper')
    parser.add_argument('--team-list', type=argparse.FileType('r'), required=True, help="File with teamname list")
    parser.add_argument('--team-ip', type=str, default="127.0.0.ID", help="Team IP Template")
    parser.add_argument('--service-list', type=argparse.FileType('r'), required=True, help="File with service,port,checker list")
    args = parser.parse_args()
    i = 0
    for team in args.team_list.readlines():
        result_json['teams'].append(
            {
                "name":team.strip(), 
                "host": args.team_ip.replace('ID',str(i)),
                "token": ''.join(secrets.choice(alphabet) for i in range(12))
            }
            )
        i+=1
    for service in args.service_list.readlines():
        name, port, checker_file = service.split(',')
        result_json['services'].append(
            {
                "name": name,
                "port": port,
                "checker_file": checker_file.strip()
            }
        )
    
    print(json.dumps(result_json, indent=2))