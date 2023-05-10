import os
from io import StringIO
from helpers import print_time_spent
from node import Node
from tqdm import tqdm


def add_pad(string: str):
    padding = (8 - len(string) % 8) % 8
    return '{0:08b}'.format(padding) + string + '0' * padding


class Compression:

    def __init__(self):
        self.symbols_count = 0
        self.table_of_codes = {}
        self.char_freq = {}
        self.nodes = []

    def create_huffman_tree(self):
        while len(self.nodes) != 1:
            self.nodes.sort(key=lambda x: x.freq)
            parent = Node(left=self.nodes[0], right=self.nodes[1])
            self.nodes.append(parent)
            del self.nodes[:2]

    def add_header_info(self):
        symbol_codes = StringIO()
        if self.nodes[0] is not None:
            self.build_header(self.nodes[0], symbol_codes)
        else:
            raise Exception('There are no nodes to build header!!!')
        head = symbol_codes.getvalue()
        self.validate_header(head)
        head_encoded = head.encode('utf8')
        # 4 bytes to store count of other header bytes (without self 4 bytes)
        tree_info = len(head_encoded)
        info_encoded = tree_info.to_bytes(4, 'big')
        return info_encoded + head_encoded

    def build_header(self, node: Node, current_header: StringIO):
        if node.left == node.right is None:
            current_header.write('1' + node.letter)
        else:
            current_header.write('0')
            self.build_header(node.left, current_header)
            self.build_header(node.right, current_header)

    @print_time_spent(message="to encode file")
    def encode(self, file):
        bits_io = StringIO()
        pbar = tqdm(total=self.symbols_count, desc="Encoded symbols")
        for line in file:
            bits_io.write(''.join(self.table_of_codes[ch] for ch in line))
            pbar.update(len(line))
        pbar.close()
        bits = add_pad(bits_io.getvalue())
        arr_header = bytearray(self.add_header_info())
        b_arr = bytearray((int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8))
        return arr_header + b_arr

    def validate_header(self, header):
        unique_symbols = len(self.char_freq.keys())
        zeros_count = unique_symbols - 1
        ones_count = unique_symbols
        if self.char_freq.keys().__contains__('0'):
            zeros_count += 1
        if self.char_freq.keys().__contains__('1'):
            ones_count += 1
        if header.count('1') != ones_count or header.count('0') != zeros_count:
            raise Exception('header is invalid')

    @print_time_spent(message="to compress file")
    def compress(self, source: str, dest: str):
        self.define_freq(source)
        self.nodes = [Node(letter=k, freq=v) for k, v in self.char_freq.items()]
        self.create_huffman_tree()
        if len(self.char_freq.keys()) == 1:
            self.create_table_of_codes(self.nodes[0], '0')
        else:
            self.create_table_of_codes(self.nodes[0], '')
        self.validate_table_of_codes()
        with open(source, "r") as f_in, open(dest, "wb") as f_out:
            byte_arr = self.encode(f_in)
            f_out.write(bytes(byte_arr))

    def validate_table_of_codes(self):
        for key, value in self.table_of_codes.items():
            if value == '':
                raise Exception('symbol \"' + key + '\" doesn\'t have a code')

    @print_time_spent(message="to define symbols frequency")
    def define_freq(self, path: str):
        with open(path, "r") as f:
            pbar = tqdm(total=float(os.path.getsize(path) / 1024 / 1024),
                        unit="Mb", unit_scale=True,
                        desc="Read to define frequency")
            for line in f:
                for ch in list(line):
                    self.char_freq.setdefault(ch, 0)
                    self.char_freq[ch] += 1
                mbytes_read = len(line.encode('utf-8')) / 1024 / 1024
                pbar.update(mbytes_read)
            pbar.close()
        if len(self.char_freq) == 0:
            raise Exception("Source file is empty")
        print(f"--- {len(self.char_freq)} different symbols ---")
        self.symbols_count = sum(v for v in self.char_freq.values())

    def create_table_of_codes(self, n: Node, code: str):
        if n.left == n.right is None:
            self.table_of_codes[n.letter] = ''.join(str(x) for x in code)
        else:
            self.create_table_of_codes(n.left, code + '0')
            self.create_table_of_codes(n.right, code + '1')
