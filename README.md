1) run weather_data_model.py to initiate the db and whenever anychanges are made to columns make sure to run this so updates can be made. 
2) run the injestion script which will load and also do the aggregate calculations on the db data
3) run the api program to get the info from swagger json file and create an api for the data

AWS deployement
1) for database we can use an rds database such as postgresql and migrate the sqllite schema into it
2) we can create a lambda function for injestion/aggregation script and we can schedulean event based trigger like SNS with SQS to run the lambda
3) we can either containerize the flask api program using docker in ECS or we can use Lambda and apigateway 
4) we can use aws cloudwatch for logging and monitoring the program. 
