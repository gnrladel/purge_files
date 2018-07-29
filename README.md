-This script is used to purges log files inside a directory , it can be used for log rotation, compression , deletion of files recursively, the configuration
is based on a xml file where we define the section for paths to purge files inside , here is an example :




<FilesConfig>
<Types>
	<Type id="1">
       <LocalDir>/tmp/dir1</LocalDir>
       <FileNameRegEx>^file_\d+.log$</FileNameRegEx>
       <RecursiveFlag>1</RecursiveFlag>
       <Compression enable="1">
       				<SkipCompressFiles>3</SkipCompressFiles>
       </Compression>
       <LeaveLastFilesNum>27</LeaveLastFilesNum>
	</Type>
	<Type id="2">
		<LocalDir>/tmp/dir2</LocalDir>
		<FileNameRegEx>^file_err_\d+.log$</FileNameRegEx>
		<RecursiveFlag>0</RecursiveFlag>
		<Compression enable="1">
					<SkipCompressFiles>3</SkipCompressFiles>
		</Compression>
		<LeaveLastFilesNum>27</LeaveLastFilesNum>
	</Type>
</Types>
</FilesConfig>


-the xml file can be put in any path, but you must configure this path inside the script :

------------------------------------------
ConfigFile='/etc/ocpurge_logs.cfg.xml'
------------------------------------------


-the script can be run using :
python file_purge.py
