import boto3
import time

# Instantiate Client for RDS
rds = boto3.client('rds')

#User defined varaibles
username = 'rdcuser'
password = 'password'
db_subnet_group = 'vpc-abb'
db_cluster_id='rds-cluster-ab'

# Create DB Cluster
try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(f"The DB cluster named {db_cluster_id} already exists. Skipping creation.")



except rds.exceptions.DBClusterNotFoundFault:
        response = rds.create_db_cluster(
        DBClusterIdentifier='my-db-cluster',
        Engine='aurora-mysql',
        EngineVersion='5.7.mysql_aurora.2.08.3',  # Corrected the typo in EngineVersion
        DBClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName='rds-hol',
        DBSubnetGroupName=db_subnet_group,
        EngineMode='serverless',
        EnableHttpEndpoint=True,
        ScalingConfiguration={
            'MinCapacity': 1,
            'MaxCapacity': 8,
            'AutoPause': True,
            'SecondsUntilAutoPause': 300
        }
    )

print(f"DB cluster named {db_cluster_id} has been created")

#Wait for DB cluster to become available

while True:
      response = rds.describe_db_cluster(DBClusterIdentifier=db_cluster_id)
      status = response['DBClusters'][0]['Status']
      print("The status of the cluster is {status}")
      if status == 'available':
            break
      
      print("Waiting for DB cluster to become available...")
      time.sleep(48)


# Modify DB Cluster. Update the scaling configuration for the cluster

response = rds.modify_db_cluster(
        
        DBClusterIdentifier=db_cluster_id,
    
        ScalingConfiguration={
            'MinCapacity': 1,
            'MaxCapacity': 16,
            'AutoPause': True,
            'SecondsUntilAutoPause': 600
        }
    )

print(f"Updated scaling configuration for DB cluster named {db_cluster_id}")


# Delete the DB cluster

response = rds.delete_db_cluster(
        
        DBClusterIdentifier=db_cluster_id,
        SkipFinalSnapshot=True
    )

print(f"The {db_cluster_id} is being deleted")

