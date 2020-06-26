#!/usr/bash

mode=all

help()
{
    echo 'Please enter the mode parameters: --all or --single or --metrics'
	echo 'sh build.sh -a/-s/-m'
	exit 0;
}

usage()
{
   echo usage: "sh build.sh [ -a ] [ --all ] all compile"
   echo "       sh build.sh [ -s ] [ --single ] compile server and agent"
   echo "       sh build.sh [ -m ] [ --metrics ] compile metrics and logsearch and infra"
   echo "       sh build.sh [ -h ] [ --help ] help "
}

while [ "$1" != "" ]; do
    case $1 in
        -a | --all )           shift
                                mode=all
                                ;;
        -s | --single )    mode=single
                                ;;
        -m | --metrics)   mode=metrics
                                ;;
        -h | --help )      	    help
			   	            exit
                                ;;
        * )                     usage
                            exit 1
    esac
    shift
done

echo "Run mode: $mode"

echo "set build version"
mvn versions:set -DnewVersion=2.7.4.0.0
pushd ambari-metrics
mvn versions:set -DnewVersion=2.7.4.0.0
popd
pushd ambari-infra
mvn versions:set -DnewVersion=2.7.4.0.0
popd

echo "set npm registry"
npm config set registry https://registry.npm.taobao.org

if [ $mode == "metrics" ]; then
    echo 'Run mode: ' $mode
    pushd ambari-metrics
    mvn clean package -Dbuild-rpm -DskipTests
    popd

    pushd ambari-logsearch
    mvn -Dbuild-rpm clean package -DskipTests
    popd

    pushd ambari-infra
    mvn clean package -Dbuild-rpm -DskipTests -Drat.skip=true
    popd

    pushd contrib/views
    mvn clean package rpm:rpm -DskipTests -Drat.skip
    popd
fi

if [ $mode == "all" ]; then
	echo 'Run mode: ' $mode
	mvn -B clean install package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=ANYSCALE -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip
fi

if [ $mode == "single" ]; then
	echo 'Run mode: ' $mode
	mvn -B -pl ambari-server clean install  package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=ANYSCALE -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip
	sleep 3
	mvn -B -pl ambari-agent clean install  package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=ANYSCALE -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip
fi
