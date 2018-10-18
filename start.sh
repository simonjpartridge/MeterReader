echo "updating git"
git pull
echo "finished updating git"
python server/server.py &
python reader/reader.py & 
echo "launched server and reader"
