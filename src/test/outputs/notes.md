I noticed that the pdf of("قانون العمل") the best result was using pymupdf by blocks


| index | meaning                           |
| ----- | -------------------------------- |
| b[0]  | x0 (horizontal position at start of the block)  |
| b[1]  | y0 (vertical position at start of the block) |
| b[2]  | x1 (end of the block horizontally )         |
| b[3]  | y1 (end of the block vertically)        |
| b[4]  | **the text inside the block**             |
| b[5]  | block number/order                 |
| b[6]  | type of the block(text / image / etc)  |

