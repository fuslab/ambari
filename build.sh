mvn -B -pl ambari-server clean install  package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=JDP -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip

mvn -B -pl ambari-agent clean install  package rpm:rpm -DnewVersion=2.7.4.0.0 -Dstack.distribution=JDP -DbuildNumber=631319b00937a8d04667d93714241d2a0cb17275 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip
