# OneProxy

Frontend runs on python v3.6.9 and Backend runs on node v12.17.0.

## Installation

```
$ git clone git@github.com:evanrolfe/oneproxy-python.git
$ cd oneproxy-python
$ (cd src/backend; npm install)
$ scripts/compile_backend.sh
$ ./run.sh
```

## Contributing

**Frontend**

Changes to the .ui files in `src/frontend/ui` or asset files in `src/frontend/assets` need to be compiled to python files using these commands:
```
$ scripts/compile_frontend_ui.sh
$ scripts/compile_frontend_assets.sh
```

**Backend**

Compile the nodejs backend server to a single binary using this command:
```
$ scripts/compile_backend.sh
```

## Test

The integration tests require that you are running the [example app](https://github.com/evanrolfe/example_app), follow those instructions to download and run it using docker. Currently the tests need to be run individually (`npm run test` will not work). So you can run them like:
```bash
$ cd src/backend
$ npm run test test/integration/browsing.js
```

## Notes

Icons come from:
https://icons8.com/icon/set/console/dusk
https://www.flaticon.com/search?word=terminal
