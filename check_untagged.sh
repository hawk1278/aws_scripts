#!/bin/bash
##################################
#                                #
# Script that receives a tag key #
# and returns its value          #
##################################
#                                #
# Example: get_tags.sh -t MyTag  #
#                                #
##################################

DATE=$(date '+%D%M%Y')
REGION=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep -i region | awk -F \" '{print $4}')
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document/ | grep -i instanceid | awk -F \" '{print $4}')

show_value(){
   echo $(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$1" --region=$REGION --output=text | cut -f5)
}
check_tag(){}

while getopts ":t:" opt; 
do
   case $opt in
     t)
         show_value $OPTARG
         ;;
     /?)
         echo "Unknow option." >&2
         exit 1
         ;;
     :)
         echo "Option, t, requires an argument." >&2
         exit 1
         ;;
   esac
done
