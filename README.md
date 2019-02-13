# NarrowBand Lib for Python 3

This is an easy-to-use library for Narrowband IoT applications. 

It communicates via UART with your target device.

It simplifies the setup and use, you don't have to manually send AT commands.

For beginners, use the Narrowband class with it's pre-defined methods.
If you want more freedom, feel free to check out the NarrowbandCore class.


## Requirements:

- Python >= 3
- PySerial >= 3.4

## Example:

If you use a supported board, the lib will auto-detect it:

```python
import narrowband

nb = narrowband.Narrowband()
nb.attach()
while 1:
    time.sleep(1)
```
    
For any other, defined the device and it's values (port, baudrate and timeout):

```
import narrowband

nb = narrowband.Narrowband("COM1", 9600, 1)
nb.attach()
while 1:
    time.sleep(1)
```
 
## Testing

Tested & verified Narrowband chips:

* Quectel BC68
* Quectel BC95-B8


## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License