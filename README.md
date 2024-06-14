run weather_data_model.py to initiate the db and whenever anychanges are made to columns make sure to run this so updates can be made. 
run the injestion script which will load and also do the aggregate calculations on the db data
run the api program to get the info from swagger json file and create an api for the data

AWS deployement
for database we can use an rds database such as postgresql and migrate the sqllite schema into it
we can create a lambda function for injestion/aggregation script and we can schedulean event based trigger like SNS with SQS to run the lambda
we can either containerize the flask api program using docker in ECS or we can use Lambda and apigateway 
we can use aws cloudwatch for logging and monitoring the program. 
