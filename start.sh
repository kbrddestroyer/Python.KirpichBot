export CONFIGPATH="./src/"

if [[ -z "${{ TOKEN }} ]]; then
 echo Am I deployed?
 touch ./src/botconfig.ini
 echo [BOT] >> ./src/botconfig.ini
 echo TOKEN=$TOKEN >> ./src/botconfig.ini
fi

python ./src/main.py 

