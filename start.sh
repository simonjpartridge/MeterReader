echo "updating git"
git reset --hard
git pull || echo "git full step finished"
echo "finished updating git"
python server/server.py &
python reader/reader.py & 
echo "launched server and reader"
