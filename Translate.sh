#! /bin/bash

#full_path=$(realpath $0) 
#dir_path=$(dirname $full_path)
dir_path=$(pwd)
echo $dir_path
dir_gettext=/home/pi/Python-3.10.0/Tools/i18n
echo $dir_gettext

# make pot file
$dir_gettext/pygettext.py -a -p $dir_path/locales/ $dir_path/weatherClock.py
echo "pot file generated"
sleep 1s

languages=("en_US" "en_GB" "nl_NL" "de_DE")

cd locales
for f in *.pot
do 
    fn="$(basename -s .pot $f)"
    echo "Filename is: $f"
    for lang in "${languages[@]}"
    do
        # Generate or upgrade po file
        if [[ -f "./$lang/LC_MESSAGES/$fn.po" ]]; then
            # it exist, so update po file
            pybabel update -i $fn.pot -d $dir_path/locales/ -l $lang
            #echo "po file updated" #above command already gives a message
        else
            # not available, so "generate" po file
            if [[ ! -e "./$lang/" ]]; then
                # make the directories
                mkdir $lang
                mkdir $lang/LC_MESSAGES
                echo "Language dir: $lang generated"
            fi
            # copy the pot file as po file in right dir
            cp -v "$f" ./$lang/LC_MESSAGES/$fn.po
            echo "Made po file"
        fi
    done
done
exit
