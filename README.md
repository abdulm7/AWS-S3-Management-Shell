# **How to run the S5 Shell**
 - begin by install the required libraries by running the following command: 
    - "pip3 install -r requirements.txt"
 - ensure you have your "S5-S3.conf" file in the same directory as the "s5_main.py" and "s3Functions.py"
 - Assuming your aws user's name is not "default" you will need to change the name to suit your user on lines 26 & 27 of "s5_main.py"
 - Once that is ready, simply run the command "python3 s5_main.py" to run the script
 - the shell will then accept appropriate commands
 - use "exit" or "quit" to stop the shell


# **Normal Behaviour of The Shell**
 - shell normally allows users to copy local files to their s3 buckets using absolute or relative paths
 - shell normally allows users to copy s3 objects to their local file system using abolsute or relative paths
 - shell normally allows users to create buckets in their s3 service
 - shell normally allows users to create folder/directories in their s3 buckets, this can be done using absolute or relative paths
 - shell normally allows users to change "directories" in their s3 service using "../" to go back a tier or "~" to go home.
 - Note, users may use "../../" as many times as they'd like to, using too many will result in changing to home directory.
 - shell normally allows users to view their current working directory
 - shell normally allows users to view a list of the buckets/directories/objects with the '-l' flag to provide more information.
 - shell normally allows users to copy objects from one location in their s3 to another, using absolute or relative paths.
 - shell normally allow users to delete objects from their s3 bucket using full or relative paths
 - shell norally allows users to delete buckets, as long as the users current working directory is not the bucket or inside the bucket.


# **Limitations**
- absolute path must begin with a forward slash '/'
- relative path must not begin with a forward slash '/'
    - these behaviours replicate bash & cmd
- *FOR s3delete* include '/' at end of folder/object name to reference a folder


<!-- REFERENCE: Absolute path **ALWAYS** starts with '/'-->
<!-- Relative path must not begin with '/', rather the name of the obj -->
https://askubuntu.com/questions/607413/when-to-use-a-preceding-slash-in-path-names-e-g-for-the-cd-command
