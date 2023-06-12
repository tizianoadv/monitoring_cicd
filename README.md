# monitoring_cicd

## This GitHub project contains the following directories:

- app/
- ansible/
- client/
- jenkins/
- jmeter/

## app/
This directory contains an API developed with Flask. The API receives data on port 5000 and stores it in a Redis database. The API also allows retrieving the data in the form of an HTML page.

- API Endpoints
- Retrieve all data: GET /
- Insert new data into the database: POST /data
- Retrieve data from the past hour: GET /data/hour
- Retrieve data from the past day: GET /data/day
- Retrieve data from the past week: GET /data/week
- Retrieve data from the past month: GET /data/month
- Retrieve data from the past year: GET /data/year

## client/
This directory contains Python code that sends POST requests representing environmental data (temperature, humidity, brightness, and timestamp) to the API on port 5000.

## ansible/
This directory contains a playbook to be executed for the development environment and a playbook to be used for the production environment.

## jenkins/
This directory contains all the scripts executed by Jenkins during the build, test, and push phases. It includes the Jenkinsfile that Jenkins should execute.

## jmeter/
This directory contains the test plans to be used with JMeter. It includes several tests, such as the test for an admin user, the test for a regular user, and the test for an admin user.
