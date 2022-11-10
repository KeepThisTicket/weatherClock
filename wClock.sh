# Source taken from README.md by @plotn and modified a little bit.
#cd  /home/plotn/github/weatherClock/

#Find the location of the python file from weatherClock.
cd /home/
dir_path=$(dirname $(find ./ -type f -name "weatherClock.py" | head -n 1))
echo $dir_path

#Detect python version
version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo $version
if [[ -z "$version" ]]; then
    echo "No Python detected!" 
    exit 2
fi

#Start the python script if it's not running.
while :
do
  if test "$(ps aux | grep python3 | grep weather | wc -l)" -eq "0"
  then
    python$version $dir_path & disown
  else
    echo "already started"
  fi
  sleep 5
done
