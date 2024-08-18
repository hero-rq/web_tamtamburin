(function(n) {
    "use strict";
    
    function xorOperation(a, b) {
        return a ^ b;
    }
    
    function rotateLeft(x, n) {
        return (x << n) | (x >>> (32 - n));
    }
    
    function checksumBlock(block, seed) {
        var result = seed;
        for (var i = 0; i < block.length; i++) {
            result = xorOperation(result, block[i]);
            result = rotateLeft(result, 5);
        }
        return result;
    }
    
    function stringToBlocks(str) {
        var blocks = [];
        for (var i = 0; i < str.length; i += 4) {
            blocks.push(str.charCodeAt(i) |
                        (str.charCodeAt(i + 1) << 8) |
                        (str.charCodeAt(i + 2) << 16) |
                        (str.charCodeAt(i + 3) << 24));
        }
        return blocks;
    }
    
    function calculateChecksum(str) {
        var blocks = stringToBlocks(str);
        var seed = 0x12345678;
        return checksumBlock(blocks, seed);
    }
    
    if (typeof define === "function" && define.amd) {
        define(function() { return calculateChecksum; });
    } else if (typeof module === "object" && module.exports) {
        module.exports = calculateChecksum;
    } else {
        n.simpleChecksum = calculateChecksum;
    }
}(this));
