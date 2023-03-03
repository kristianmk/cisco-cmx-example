# cisco-cmx-example
Set environment variables cmx_server, cmx_user, cmx_password, and device_hw_addr before use.


## main.py
Basic CMX useage, log wifi device position (cartesian coordinates) and scatter-plot for 60 seconds.

## mazemap_cmx.py
Mazemap + CMX with flask. Find route from wifi device position (geo coordinates) to a given (hard coded) meeting room. Note: zLevel of starting position is set to 3, so without modifications this example will only work for 3rd floor.
