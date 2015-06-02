
# by lonslonz, 2015-06-02

import sys
import arrow
import dataset
from optparse import OptionParser

def main(options, args):

    curr = arrow.utcnow()

    if(options.basis == "daily") :
        curr = curr.floor('day')
        remove = curr.replace(days=-options.removePart)
        add = curr.replace(days=+options.addPart)
    else:
        curr = curr.floor('month')
        remove = curr.replace(months=-options.removePart)
        add = curr.replace(months=+options.addPart)

    removeQuery = "alter table %s drop partition p%s" % (options.table, remove.format('YYYYMMDD'))
    addQuery = "alter table %s add partition (partition p%s values less than (unix_timestamp('%s')))" % \
               (options.table, add.format('YYYYMMDD'), add.format('YYYY-MM-DD 00:00:00'))

    uri = "mysql://" + options.user + ":" + options.password + "@" + options.host + "/" + options.db

    try:
        db = dataset.connect(uri)
    except Exception, e:
        print e.message
        return
    try:
        print "+ Remove a partition"
        print "- Query: ", removeQuery
        result = db.query(removeQuery)
        print "- Success"
    except Exception, e:
        print "- Error: ", e.message

    try:
        print "+ Add a partition"
        print "- Query", addQuery
        result = db.query(addQuery)
        print "- Success"
    except Exception, e:
        print "- Error: ", e.message

    print "Complete Work"


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
                      choices=['daily', 'monthly'], help = "time basis")

    (options, args) = parser.parse_args()
    print options
    print "database : ", options.db
    print args
    main(options, args)

