FROM quay.io/astronomer/ap-airflow:2.2.1-buster-onbuild
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libodbcinst.so
#ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib
#ENV ODBCINI=/etc/odbc.ini
#ENV ODBCINSTINI=/etc/odbcinst.ini
#ENV CLOUDERAIMPALAINI=/etc/cloudera.impalaodbc.ini
USER root
RUN apt install  /usr/local/airflow/include/clouderaimpalaodbc_2.6.11.1011-2_amd64.deb
ADD include/odbcinst.ini /etc/odbcinst.ini
ADD include/odbc.ini /etc/odbc.ini
#ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libodbcinst.so