if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	cd /home/pi/Documents/SciSpin_Max_Dev
	git pull
fi
cd /home/pi/Documents/SciSpin_Max_Dev/_python

sudo python3 Main.py > /home/pi/output.log
