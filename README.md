# TODO
1. added CI/CD (???) 
2. huffman decompress in window
3. lzw compress/decompress in terminal
4. huffman adaptive compress/decompress in terminal
5. lzw compress/decompress in window
6. huffman adaptive compress/decompress in window

# huffman_algorithm

Compressed binary string consists of:
1. header:
   
   a) count of bytes UTF-8 encoded of rest of header
   
   b) UTF-8 symbols encoded: '0', '1' or symbol
3. sequence encoded

For Linux:
1. download project
2. cd /path/to/project
3. `
python3.11 -m venv venv && 
chmod +x ./venv/bin/activate && 
./venv/bin/activate && 
./venv/bin/pip install pipenv && 
./venv/bin/python3.11 -m pip install --upgrade pip && 
./venv/bin/pipenv install && 
sudo apt-get install libxcb-cursor0
`

OPTIONAL!
   
`
./venv/bin/pipenv lock
`

4.
   a) `venv/bin/python3.11 main.py *source_path* *dest_path*` to encode;   
   or   
   b) `venv/bin/python3.11 main.py decode *source_path* *dest_path*` to decode;

5. run Window mode:
   
`
./venv/bin/python3.11 src/app_window.py
`

Edit program window:

`
./venv/bin/pyqt6-tools designer  
./venv/bin/pyuic6  src/app_window.ui -o src/app_window.py    
`

You can check:

`
venv/bin/python3 main.py tests/test_files/test2.xml tests/test_files/test2_enc && 
venv/bin/python3 main.py decode tests/test_files/test2_enc tests/test_files/test2_res ;
rm tests/test_files/test2_enc tests/test_files/test2_res
`


--- 189 different symbols ---
--- 1.4361639022827148 seconds to define symbols frequency ---
--- 2.529226064682007 seconds to encode file ---
--- 3.970651626586914 seconds to compress file ---
--- Compression: 55.02 % ---
--- 0.0037603378295898438 seconds to read all bytes from file ---
--- 4.645887851715088 seconds to decode file and write it to dest ---
--- 4.787070035934448 seconds to decompress ---
--- Compression: 55.02 % ---


STRESS TEST:

`
cat tests/test_files/test2.xml > tests/test_files/test2_tmp.xml && 
cat tests/test_files/test2.xml >> tests/test_files/test2_tmp.xml && 
cat tests/test_files/test2.xml >> tests/test_files/test2_tmp.xml  && 
venv/bin/python3 main.py tests/test_files/test2_tmp.xml tests/test_files/test2_enc && 
venv/bin/python3 main.py decode tests/test_files/test2_enc tests/test_files/test2_res.xml ;
rm tests/test_files/test2_tmp.xml tests/test_files/test2_enc tests/test_files/test2_res.xml
`

--- 189 different symbols ---
--- 4.063854217529297 seconds to define symbols frequency ---
--- 7.374655485153198 seconds to encode file ---
--- 11.4525306224823 seconds to compress file ---
--- Compression: 55.02 % ---
--- 0.009339570999145508 seconds to read all bytes from file ---
--- 14.517167091369629 seconds to decode file and write it to dest ---
--- 14.935723304748535 seconds to decompress ---
--- Compression: 55.02 % ---
