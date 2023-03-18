# Download Boditrax Data

This python API allows you to download data from Boditrax in a dataframe format and then save it in csv. 

## Usage

### BODITRAX 2
```
b = Boditrax2()
b.get_from_cloud()
df = b.to_dataframe()
df.to_csv('boditrax2.csv')
```
use ```year``` as argument to ```get_from_cloud( year )``` to get values in the past

### BODITRAX 1
```
b = Boditrax()
b.get_from_cloud()
df = b.to_dataframe()
df.to_csv('boditrax1.csv')
```

## Authentication

This uses the browser_cookie3 library for gathering cookies from your local browser for interacting with boditrax.

## Contributing

If you would like to contribute to the development of this API, please feel free to fork the repository and submit pull requests. We welcome any contributions that will help improve the functionality of the API.

## Support

If you have any questions or issues using this API, please open an issue in the repository or contact the developer directly.