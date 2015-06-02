# PartitionRoller
Roll MySQL partitions periodically. It drops previous partitions and adds new partitions. 

### Install 

Download source and execute rollPartition.py or register it to your cron

### Creating MySQL partitioned table

To maintain tables for historic data (You want to remove the partition which is 3 days ago, and create new partition for next day), I highly recommend using follow schemas to make the partitioned table. Just choose daily or monthly creation. It depends on data size.

        CREATE TABLE `daily_partitioned_table` (
          `a` bigint(20) NOT NULL AUTO_INCREMENT,
          `b` bigint(20) NOT NULL,
          `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`a`,`update_time`)
        ) ENGINE=InnoDB
        /*!50100 PARTITION BY RANGE (UNIX_TIMESTAMP(update_time))
        (PARTITION p20150529 VALUES LESS THAN (unix_timestamp('2015-05-29 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150530 VALUES LESS THAN (unix_timestamp('2015-05-30 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150531 VALUES LESS THAN (unix_timestamp('2015-05-31 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150601 VALUES LESS THAN (unix_timestamp('2015-06-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150602 VALUES LESS THAN (unix_timestamp('2015-06-02 00:00:00')) ENGINE = InnoDB) */;
 
        CREATE TABLE `monthly_partitioned_table` (
          `a` bigint(20) NOT NULL AUTO_INCREMENT,
          `b` bigint(20) NOT NULL,
          `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`a`,`update_time`)
        ) ENGINE=InnoDB
        /*!50100 PARTITION BY RANGE (UNIX_TIMESTAMP(update_time))
        (PARTITION p20150101 VALUES LESS THAN (unix_timestamp('2015-01-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150201 VALUES LESS THAN (unix_timestamp('2015-02-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150301 VALUES LESS THAN (unix_timestamp('2015-03-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150401 VALUES LESS THAN (unix_timestamp('2015-04-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150501 VALUES LESS THAN (unix_timestamp('2015-05-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150601 VALUES LESS THAN (unix_timestamp('2015-06-01 00:00:00')) ENGINE = InnoDB,
         PARTITION p20150701 VALUES LESS THAN (unix_timestamp('2015-07-01 00:00:00')) ENGINE = InnoDB) */;
         
### Executing roller

execute rollPartition.py script with arguements.

        python rollPartition.py -H mysql.server.com -d database -u username -p password -r 4 -a 3 -b monthly -t t2

* -H : MySQL server
* -d : database
* -u : user
* -p : password
* -r : the partition to be removed (day or month)
* -a : the partition to be added (day or month)
* -b : monthly or daily 

### Example

Assume that today is 2015-03-04. I want to maintain historic data for 3 days. And create a partition in advance. Following execution will remove the partition of 2015-03-01 and create the partitions of 2015-03-07

        python rollPartition.py -H mysql.server.com -d database -u username -p password -r 3 -a 3 -b daily -t t1
        
I want to maintain historic data for 3 months. Following execution will remove the partition of 2015-01-01 and create the partitions of 2015-05-01

        python rollPartition.py -H mysql.server.com -d database -u username -p password -r 2 -a 2 -b daily -t t2

### Register to crontab

Register it like this. Recommend executing it every day.

        00 10 * * * python /your/script/rollPartition.py -H mysql.server.com -d database -u username -p password -r 2 -a 2 -b monthly -t t2 >> exe.log
