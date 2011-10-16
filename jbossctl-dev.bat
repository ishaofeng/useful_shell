@echo off
@if not "%ECHO%" == ""  echo %ECHO%
@if "%OS%" == "Windows_NT"  setlocal

set ENV_PATH=.\
if "%OS%" == "Windows_NT" set ENV_PATH=%~dp0%
call %ENV_PATH%\env.bat

REM copy file to jboss server home.

COPY  "%SEARCH_HOME%\conf\jboss\conf\props\console-users.properties"  "%JBOSS_SERVER_HOME%\conf\props\console-users.properties" /Y
COPY  "%SEARCH_HOME%\conf\jboss\conf\jboss-service.xml"  "%JBOSS_SERVER_HOME%\conf\jboss-service.xml" /Y
COPY  "%SEARCH_HOME%\conf\jboss\deploy\tomcat-jboss-service.xml" "%JBOSS_SERVER_HOME%\deploy\jbossweb-tomcat55.sar\META-INF\jboss-service.xml" /Y
COPY  "%SEARCH_HOME%\conf\jboss\deploy\web.xml"  "%JBOSS_SERVER_HOME%\deploy\jbossweb-tomcat55.sar\conf\web.xml"  /Y
COPY  "%SEARCH_HOME%\conf\jboss\deploy\tomcat-server.xml" "%JBOSS_SERVER_HOME%\deploy\jbossweb-tomcat55.sar\server.xml" /Y
REM antxexpand "%SEARCH_HOME%\target\search-bundle-war.war" "%JBOSS_SERVER_HOME%\deploy\web\"
REM antxexpand "D:\work_space\workshop-3\target\workshop-webapp-2.war" "%JBOSS_SERVER_HOME%\deploy\web\"
COPY "D:\work_space\workshop-3\target\workshop-webapp-2.war" "%JBOSS_SERVER_HOME%\deploy\web.war"
REM COPY  "%SEARCH_HOME%\target\search-bundle-war.war"  "%JBOSS_SERVER_HOME%\deploy\web.war" /Y
REM echo "%SEARCH_HOME%\target\search-bundle-war\"
REM echo "%JBOSS_SERVER_HOME%\deploy\web"
REM XCOPY "%SEARCH_HOME%\target\search-bundle-war\*.*"  "%JBOSS_SERVER_HOME%\deploy\web\" /Y /E
REM cls screen 
rem CLS

set JAVA_OPTS= %JAVA_OPTS% %JAVA_MEM_OPT% %JBOSS_SERVER_DIR% %JAVA_DEBUG_OPT% 

call %JBOSS_HOME%\bin\run.bat
