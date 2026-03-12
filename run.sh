# initialize conda for bash
source ~/miniconda3/etc/profile.d/conda.sh

conda activate slack_bot
cd slackbot
python manage.py runserver