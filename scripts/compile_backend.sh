cp src/backend/node_modules/sqlite3/lib/binding/node-v72-linux-x64/node_sqlite3.node ./build/node_sqlite3.node

ORIGINAL="var binding = require(binding_path);"
CHANGED="var binding = require(\'.\/node_sqlite3.node\')"

sed -i "4s/.*/$CHANGED/g" src/backend/node_modules/sqlite3/lib/sqlite3.js

pkg ./src/backend/index.js --output=./build/oneproxy-backend -t node12-linux-x64

# Revert it back to original state:
sed -i "4s/.*/$ORIGINAL/g" src/backend/node_modules/sqlite3/lib/sqlite3.js
