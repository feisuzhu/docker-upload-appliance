docker-upload-appliance
=======================

This is a appliance handling file uploading, compatible with [jQuery-File-Upload](http://blueimp.github.io/jQuery-File-Upload/).

Config
------

#### /upload/upload.json
    {
      "prefix": "http://localhost:4444/files/",  // uploaded file url prefix
      "max_size": 5242880,  // Maximum file size
      "can_delete": true  // Can delete uploaded file?
    }

#### /upload/files
This is where uploaded file stored.
You should make this directory a volume.

#### /upload/cors.conf
Just snippet of nginx conf.
By default there is only one directive `more_set_headers "Access-Control-Allow-Origin: *";`
You can ignore this if CORS doesn't make sense to you or the default is what you want.

Example
-------

    git clone https://github.com/feisuzhu/docker-upload-appliance
    cd docker-upload-appliance
    docker build -t uploadapp .
    docker run \
        --name my_upload_app
        -d
        -p 8888:80
        -v /data/data/upload:/upload/files
        -v /data/etc/upload/upload.json:/upload/upload.json
        -v /data/etc/upload/cors.conf:/upload/cors.conf
        uploadapp

Now you can `proxy_pass` your nginx to port `8888`.
Try it with [jQuery-File-Upload](http://blueimp.github.io/jQuery-File-Upload/).

In above example, your uploaded files will be stored at `/data/data/upload` on host.
Configs located at `/data/etc/upload/upload.json` and `/data/etc/upload/cors.conf` on host.


Other words
-----------

Only allowing images uploads, you can hack it if you want to allow other files.
Thumbnail feature not implemented, just returning original image url.

This appliance is not mature, since it's a byproduct of my Docker learning process.
I'll continue maintaining it when I need this, or there's enough people interested.
