### Format of the data

Each .nc.tar file contains a range of forecasts.
The range contained can be determined from the filename.

All filenames follow this format, with the sections `[FORECAST_START]`,
`[FORECAST_END]` and `[REQ_ID]` filled in.
 
`gfs.0p25.[FORECAST_START]-[FORECAST_END].grib2.[REQ_ID].nc.tar`

#### `[REQ_ID]`
The unique identifier of the request submitted to UCAR.
For our data, it will always be "panzer408979".

#### `[FORECAST_START]` and `[FORECAST_END]`
Use the following format to indicate the beginning and 
end of the forecast range:

`<YYYY><MM><DD><HH>.f<hhh>`
- `<YYYY>` = four digit year
- `<MM>` = 2 digit month  (00, 01...11, 12)
- `<DD>` = 2 digit day (01, 02...29, 30, 31)
- `<HH>` = 2 digit 24-hour hour
- `<hhh>` = 3 digit number of hours in the future which the forecast
applies to

For example, `2018 12 25 06.f165` (spaces added for readability)
indicates a forecast that was made on December 25th, 2018, at 06:00
which predicted the weather 165 hours in the future, ie
January 1st, 2019 at 03:00.