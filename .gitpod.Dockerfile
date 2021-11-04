FROM gitpod/workspace-full
                
USER root
RUN sudo apt-get update
RUN sudo apt-get install psycopg2 libpq-dev python-dev
