
# by lonslonz, 2015-06-02

import sys
import arrow
import dataset
from optparse import OptionParser

def main(options, args):

    curr = arrow.now()
    print ("Current time : ", curr)

    if(options.basis == "daily") :
        curr = curr.floor('day')
        remove = curr.replace(days=-options.removePart)
        add = curr.replace(days=+options.addPart)
        partitionNameFormat = 'YYYYMMDD'
        timeFormat = 'YYYY-MM-DD 00:00:00'
    elif(options.basis == "monthly"):
        curr = curr.floor('month')
        remove = curr.replace(months=-options.removePart)
        add = curr.replace(months=+options.addPart)
        partitionNameFormat = 'YYYYMMDD';
        timeFormat = 'YYYY-MM-DD 00:00:00'
    else:
        curr = curr.floor('hour')
        remove = curr.replace(hours=-options.removePart)
        add = curr.replace(hours=+options.addPart)
        partitionNameFormat = 'YYYYMMDDHH'
        timeFormat = 'YYYY-MM-DD HH:00:00';

    removeQuery = "alter table %s drop partition p%s" % (options.table, remove.format(partitionNameFormat))
    addQuery = "alter table %s add partition (partition p%s values less than (unix_timestamp('%s')))" % \
           (options.table, add.format(partitionNameFormat), add.format(timeFormat))

    uri = "mysql://" + options.user + ":" + options.password + "@" + options.host + "/" + options.db

    try:
        if not options.verbose :
            db = dataset.connect(uri)
    except Exception as e:
        print (e)
        return
    try:
        print ("+ Remove a partition")
        print ("\t- Query: ", removeQuery)
        if not options.verbose :
            result = db.query(removeQuery)
        print("\t- Success")
    except Exception as e:
        print("\t- Warn: ", e)

    try:
        print("+ Add a partition")
        print("\t- Query", addQuery)
        if not options.verbose :
            result = db.query(addQuery)
        print ("\t- Success")
    except Exception as e:
        print ("\t- Warn: ", e)

    print ("Complete Work")


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-H", "--host", action = "store", type = "string", dest = "host",
                      help = "MySQL database name")
    parser.add_option("-d", "--database", action = "store", type = "string", dest = "db",
                      help = "MySQL Server Address")
    parser.add_option("-t", "--table", action = "store", type = "string", dest="table",
                      help = "MySQL Table")
    parser.add_option("-u", "--user", action = "store", type = "string", dest="user",
                      help = "MySQL User Id")
    parser.add_option("-p", "--password", action = "store", type = "string", dest="password",
                      help = "MySQL User Password")
    parser.add_option("-a", "--add", action = "store", type = "int", dest="addPart",
                  help = "a partition to be added ")
    parser.add_option("-r", "--remove", action = "store", type = "int", dest="removePart",
                  help = "a partition to be removed")
    parser.add_option("-b", "--basis", action = "store", type = "choice", dest="basis", default="daily",
                      choices=['daily', 'monthly', 'hourly'], help = "time basis")
    parser.add_option("-v", "--verbose", action = "store_true", dest="verbose", default=False, help = "only print query")

    (options, args) = parser.parse_args()
    print (options)
    print ("database : ", options.db)
    print (args)
    main(options, args)

