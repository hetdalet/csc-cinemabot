import os
import subprocess
import sys


def run_test_env_container():
    tests_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    project_path = os.path.join(tests_dir, '..')
    project_path = os.path.abspath(project_path)
    args = [
        'docker',
        'run',
        '-it',
        '--rm',
        '-v', rf'{project_path}/tests:/opt/csc-cinemabot/tests',
        '-v', rf'{project_path}/app:/opt/csc-cinemabot/app',
        'csc-cinemabot-test:latest'
    ]
    subprocess.run(args, check=True)


if __name__ == '__main__':
    run_test_env_container()
