# S3 Stress Test

A simple python script to test read/write capabilities of your s3 compatible storage (eg. Ceph)

### Prerequisites

This script is written and tested for Python3.8
Before you run it you need to install few dependecies listed on the file requirements.txt

On a virtualenv or your base system run:
```
pip3 install -r requirements.txt

```

### Usage

The script was written to be used by a devops or sysadmin so all the configuration is passed at runtime using switches.
Could be extended in the future with config files or env vars.

Example of a read test:
```
python3 s3_stress_test.py --url s3.scalablestorage.it --access-key theuseraccesskey --secret-key thesupersecretkey --bucket nostress --read /
```

Example of a write test:
```
python3 s3_stress_test.py --url s3.scalablestorage.it --access-key theuseraccesskey --secret-key thesupersecretkey --bucket nostress --write --file-size 8192 --num-files 100
```

Example of a write/read test:
```
python3 s3_stress_test.py --url s3.scalablestorage.it --access-key theuseraccesskey --secret-key thesupersecretkey --bucket nostress --write --read /
```



For huge file numbers or huge buckets i reccomend using tmux

#### Options ####

| Parameter                     | Example                | Description  |	
| :-----------------------------|:----------------------:|:-------------|
| --url **(required)** 	        |	s3.scalablestorage.it  | url where your s3 storage reside |
| --access-key **(required)**   | user                   | the s3 user access key |
| --secret-key **(required)** 	|	secret                 | number of cores to be used |
| --bucket **(required)**  		  | mybucket	             | the bucket to use for test |
| --read 		                    |                        | peform a list on all files in the bucket |
| --read-max-files              | 1000                   | maximum number of files to read (needed because s3 module does not take infinite number)
| --write                       |                        | perform a write operation, if read and write are used together will perform both in the order write/read |
| --write-files                 | 3                      | number of files to be write **(default 1)** |
| --file-size                   | 8192                   | file size in bytes to use for write test **(default 8192 (8K))** |
| --files-per-folder            | 100                    | optional argument if you want to organize the files in various folders (useful to simulate a non-flat bucket with milions of files)
| --log-level                   | INFO                   | this will show some output but be careful it can slow down the execution especially for large operations.


## Considerations

The script was written for infrastrucutre admins to benchmark or troubleshoot their own storage.
If used against public service providers could result in a very expensive bill, use it at your own risk.

## Contributing

Anyone is free to contribute, any suggestion for improvment is much welcome



## Authors

* Giordano Corradini - *Initial work*


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details
