#!/usr/bash

mode=all

help()
{
	if [ "$1" == "" ]; then
		echo 'Please enter the mode parameters: all or single'
		echo 'sh build.sh -a/-s'
		exit 0;
	fi
}

while [ "$1" != "" ]; do
    case $1 in
        -a | --all )           shift
                                mode=all
                                ;;
        -s | --single )    mode=single
                                ;;
        -h | --help )      	help
			   	exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

echo "Run mode: $mode"

mvn versions:set -DnewVersion=2.7.4.0.0

if [ $mode == "all" ]; then
	echo 'Run mode: ' $mode
	mvn -B clean install package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=HDP -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip -Preplaceurl
fi

if [ $mode == "single" ]; then
	echo 'Run mode: ' $mode
	mvn -B -pl ambari-server clean install  package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=HDP -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip
	sleep 3
	mvn -B -pl ambari-agent clean install  package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=HDP -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip
fi
