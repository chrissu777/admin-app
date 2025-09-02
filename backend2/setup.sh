sigint_handler(){
	sudo fuser -k 8000/tcp
	trap - INT
	kill -INT "$$"
}
trap sigint_handler INT
docker compose up -d
python manage.py runserver &
while true
do
        python manage.py populaterecordings
        sleep 5
done

