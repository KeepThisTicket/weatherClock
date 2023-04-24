#! /bin/bash

#Get current path
#full_path=$(realpath $0) 
#dir_path=$(dirname $full_path)
dir_path=$PWD
echo $dir_path

#Search gettext
pushd ~
dir_gettext=$(find -name "pygettext.py" -type f | head -n 1)    #./home/pi/Python-3.10.0/Tools/i18n/pygettext.py
#echo $dir_gettext
dir_gettext="$(dirname "$dir_gettext")" #remove filename
echo $dir_gettext
if [[ 0 != $? ]] || [[ -z $dir_gettext ]] ; then
    echo "No gettext library found."
    echo "Program Translate ends."
    exit 5
fi
#popd    #cd $dir_path
    
# make *.pot file
$dir_gettext/pygettext.py -a -p $dir_path/locales/ $dir_path/weatherClock.py
echo "pot file generated"
sleep 1s

languages=("en_US" "en_GB" "nl_NL" "de_DE")

# make or update foreach pot file a translate po file.
cd $dir_path/locales
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

# Wait until user has updated the po files.
echo "" #empty line
echo "Change/ update the po files now and when finished continue to generate mo files out of it."
echo "Press any key to continue"
while [ true ] ; do
    read -t 3 -n 1
    if [[ $? == 0 ]] ; then
        break
    fi
done

cd ~
#Generate mo files
for lang in "${languages[@]}"
do
    # Check po file available
    if [[ -f "$dir_path/locales/$lang/LC_MESSAGES/$fn.po" ]]; then
        # it exist, so make mo file
        "$dir_gettext/msgfmt.py" -o "$dir_path/locales/$lang/LC_MESSAGES/$fn.mo" "$dir_path/locales/$lang/LC_MESSAGES/$fn"
        echo "$fn.mo file in language $lang updated"
    fi
done
exit
