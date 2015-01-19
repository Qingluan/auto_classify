#auto_classify  Document
>dependences Part
 -  pandas
	+ provide save csv and parser path data
 
## Introduction 
## Install 

<code>cp file_classify.py /usr/local/bin/ </code>

## Useage 
 
#### example

>file_classify.py  -a ~/Download   _auto classify this path's all file and dir_

>file_classify.py -a ~/Download -i "dir" _like before but will ignore some file's type_ 

>file_classify.py -a ~/Download -b _back to case before auto-classify_

    usage: it is usage for auto classify  

    this is a assistant for write web html weite by Qingluan github :
    http://github.com/Qingluan

    optional arguments:
    -h, --help            show this help message and exit
    -a NAME_PATH, --name_path NAME_PATH
                        this argu is represent dir name
                        example "file_classify.py -a ~/Download "
                        this is the most easy way to use 
    -b, --backup          if -a and -b ,will back to position before classified
                        after classified ,if you regred it , you can use it to back to last version 
                        because auto_classify will record in ~/.auto_**
    -c CLEAR_PATH, --clear_path CLEAR_PATH
    -r, --recursion
    -d, --debug
    -i IGNORE, --ignore IGNORE
